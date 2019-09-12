Verify that beets works

  $ beet version >/dev/null
  $ echo $?
  0

Set up initial beets configuration

  $ export BEETSDIR="$PWD"
  $ cat >"$PWD/config.yaml" <<END
  > directory: .
  > plugins: replace_format
  > num_replace:
  >   '250': '500'
  > path_replace:
  >   '^data': 'newdata'
  > END

Set up library

  $ beet import -qCWA "$TESTDIR/data/250-milliseconds-of-silence.mp3" >/dev/null 2>&1
  $ beet ls
  Anar Software LLC - Blank Audio - 250 Milliseconds of Silence

Test %replace

  $ beet ls -f '%replace{num_replace,$title}'
  500 Milliseconds of Silence

Test %replace_path

  $ beet ls -f '%replace_path{path_replace,$path}' | sed -e "s#${TESTDIR%/data}/##"
  newdata/250-milliseconds-of-silence.mp3

Test %sub

  $ beet ls -f '%sub{$title,Silence,Noise}'
  250 Milliseconds of Noise
