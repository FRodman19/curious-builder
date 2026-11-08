#!/usr/bin/env python3
"""Render plain text with an installed macOS voice; no downloads or API calls.

Input: [{"id": "intro", "text": "Open the project.", "evidence": ["source"]}]
Requires macOS /usr/bin/say and existing ffmpeg/ffprobe executables.
"""
import argparse
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


def run(args):
    return subprocess.run(args, check=True, text=True, capture_output=True)


def voices():
    found = []
    for line in run(['/usr/bin/say', '-v', '?']).stdout.splitlines():
        match = re.match(r'^(.+?)\s+([a-z]{2,3}_[A-Za-z0-9_-]+)\s+#', line)
        if match and (match[1].strip(), match[2]) not in found:
            found.append((match[1].strip(), match[2]))
    return found


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, help='UTF-8 JSON array, or object with lines array')
    parser.add_argument('--out', type=Path, help='New/empty output directory')
    parser.add_argument('--preset', type=Path, help='Reusable JSON voice/rate/gap/normalization/trim settings')
    parser.add_argument('--voice', help='Installed voice name; use --list-voices')
    parser.add_argument('--rate', type=int, help='Speech rate in words per minute')
    parser.add_argument('--gap', type=float, help='Suggested inter-line gap, not baked into WAVs')
    parser.add_argument('--gain-db', type=float, help='Optional attenuation trim from -24 to 0 dB')
    parser.add_argument('--normalize', action=argparse.BooleanOptionalAction, default=None, help='Peak normalization to -3 dBFS, max +6 dB gain')
    parser.add_argument('--list-voices', action='store_true')
    args = parser.parse_args()
    defaults = {'voice': 'Samantha', 'rate': 165, 'gap': 0.25, 'normalize': False, 'gain_db': 0.0}
    preset = json.loads(args.preset.read_text(encoding='utf-8')) if args.preset else {}
    if not isinstance(preset, dict) or set(preset) - (set(defaults) | {'pronunciation_notes'}):
        parser.error('Preset must be an object with voice, rate, gap, normalize, gain_db or pronunciation_notes')
    for key, default in defaults.items():
        if getattr(args, key) is None:
            setattr(args, key, preset.get(key, default))
    notes = preset.get('pronunciation_notes', {})
    if not isinstance(notes, dict) or any(not isinstance(k, str) or not isinstance(v, str) for k, v in notes.items()):
        parser.error('pronunciation_notes must map words to plain-text notes; no automatic replacements are made')
    if not isinstance(args.voice, str) or type(args.rate) is not int or type(args.normalize) is not bool:
        parser.error('Preset voice must be a string, rate an integer, and normalize a boolean')
    if any(type(v) not in (int, float) or not math.isfinite(v) for v in (args.gap, args.gain_db)):
        parser.error('Gap and gain_db must be finite numbers')
    if not -24 <= args.gain_db <= 0:
        parser.error('gain_db is an attenuation trim from -24 to 0; use --normalize for measured boost')
    if sys.platform != 'darwin' or not Path('/usr/bin/say').is_file():
        parser.error('Only macOS installed system speech is implemented. No external fallback is attempted.')
    installed = voices()
    if args.list_voices:
        print(json.dumps([{'name': name, 'locale': locale} for name, locale in installed], ensure_ascii=False, indent=2))
        return
    if not args.input or not args.out:
        parser.error('--input and --out are required for generation')
    if not 80 <= args.rate <= 300 or not math.isfinite(args.gap) or args.gap < 0:
        parser.error('Use rate 80–300 and a finite nonnegative gap')
    names = [name for name, _ in installed]
    selected = args.voice if args.voice in names else next((name for name in names if name.split(' (')[0] == args.voice), None)
    if selected is None:
        parser.error('Requested voice is not listed as installed; no download or fallback is attempted')
    ffmpeg, ffprobe = shutil.which('ffmpeg'), shutil.which('ffprobe')
    if not ffmpeg or not ffprobe:
        parser.error('Install dependencies separately: existing ffmpeg and ffprobe are required')
    payload = json.loads(args.input.read_text(encoding='utf-8'))
    lines = payload.get('lines') if isinstance(payload, dict) else payload
    if not isinstance(lines, list) or not lines:
        parser.error('Input must contain a nonempty lines array')
    ids = set()
    for row in lines:
        if not isinstance(row, dict) or not isinstance(row.get('text'), str) or not row['text'].strip():
            parser.error('Each line needs nonempty plain text')
        if '[[' in row['text'] or ']]' in row['text'] or '\x00' in row['text']:
            parser.error('Speech commands and null characters are not accepted; supply plain text')
        ident = row.get('id')
        if not isinstance(ident, str) or not re.fullmatch(r'[A-Za-z0-9_-]+', ident) or ident in ids:
            parser.error('Each line needs a unique id containing letters, digits, hyphens or underscores')
        ids.add(ident)
    if args.out.exists() and any(args.out.iterdir()):
        parser.error('Output directory must be new or empty; preserve earlier narration runs')
    args.out.mkdir(parents=True, exist_ok=True)
    manifest = {'engine': 'macOS /usr/bin/say', 'voice': selected, 'rate_wpm': args.rate,
                'sample_rate': 48000, 'channels': 1, 'trim_db': args.gain_db, 'pronunciation_notes': notes,
                'preset': str(args.preset.resolve()) if args.preset else None, 'normalization': 'peak -3 dBFS, max +6 dB gain' if args.normalize else 'none',
                'gap_seconds': args.gap, 'timing_note': 'Suggested starts are cumulative measured durations plus gap; WAVs contain no added gap.',
                'input': str(args.input.resolve()), 'lines': []}
    cursor = 0.0
    with tempfile.TemporaryDirectory(prefix='app-demo-system-voice-') as tmp:
        tmp = Path(tmp)
        for i, row in enumerate(lines):
            text_file = tmp / 'line.txt'
            text_file.write_text(row['text'], encoding='utf-8')
            aiff = tmp / 'speech.aiff'
            run(['/usr/bin/say', '-v', selected, '-r', str(args.rate), '-f', str(text_file), '-o', str(aiff)])
            gain = args.gain_db
            if args.normalize:
                peak_log = run([ffmpeg, '-hide_banner', '-i', str(aiff), '-af', 'volumedetect', '-f', 'null', '-']).stderr
                match = re.search(r'max_volume:\s*(-?[\d.]+) dB', peak_log)
                if not match:
                    raise RuntimeError('Could not measure voice peak; refusing unmeasured normalization')
                gain = min(6.0, -3.0 - float(match[1])) + args.gain_db
            name = f'{i+1:03d}-{row["id"]}.wav'
            command = [ffmpeg, '-hide_banner', '-loglevel', 'error', '-y', '-i', str(aiff), '-ar', '48000', '-ac', '1']
            if args.normalize or args.gain_db:
                command += ['-af', f'volume={gain:.4f}dB']
            command += ['-c:a', 'pcm_s16le', str(args.out / name)]
            run(command)
            duration = float(run([ffprobe, '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(args.out / name)]).stdout.strip())
            if not math.isfinite(duration) or duration <= 0:
                raise RuntimeError(f'Invalid output duration for {row["id"]}')
            manifest['lines'].append({'id': row['id'], 'text': row['text'], 'evidence': row.get('evidence', []), 'file': name,
                                      'duration': duration, 'suggested_start': round(cursor, 6), 'suggested_end': round(cursor+duration, 6), 'gain_db': round(gain, 4)})
            cursor += duration + (args.gap if i < len(lines)-1 else 0)
    manifest['suggested_duration'] = round(cursor, 6)
    manifest['voice_duration'] = round(sum(row['duration'] for row in manifest['lines']), 6)
    (args.out / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'manifest': str((args.out/'manifest.json').resolve()), 'lines': len(lines), 'voice': selected, 'duration': manifest['suggested_duration']}))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        detail = exc.stderr.strip() if isinstance(exc, subprocess.CalledProcessError) and exc.stderr else str(exc)
        print(f'Voice generation failed: {detail}', file=sys.stderr)
        sys.exit(1)
