Verify that beets works

Set up initial beets configuration

  $ export BEETSDIR="$PWD"
  $ beet version >/dev/null

  $ cat >"$PWD/config.yaml" <<END
  > directory: .
  > plugins: replaceformat
  > num_replace:
  >   '250': '500'
  > path_replace:
  >   '^data': 'newdata'
  > invalid_replace:
  >   '(foo': 'bar'
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

Test %sub_path

  $ beet ls -f '%sub_path{$path,data,newdata}' | sed -e "s#${TESTDIR%/data}/##"
  newdata/250-milliseconds-of-silence.mp3

Errors

  $ beet ls -f '%sub{$title,(invalid,nothing}'
  <missing ), unterminated subpattern at position 0>

  $ beet ls -f '%sub_path{$title,(invalid,nothing}'
  <missing ), unterminated subpattern at position 0>

  $ beet ls -f '%replace{invalid_replace,$title}'
  <invalid_replace: error compiling regex `\(foo`.*> (re)

  $ beet ls -f '%replace{missing_replace,$title}'
  <missing_replace not found>
