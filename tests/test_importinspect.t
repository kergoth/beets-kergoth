Verify that beets works

Set up initial beets configuration

  $ export BEETSDIR="$PWD"
  $ beet version >/dev/null

  $ cat >"$PWD/config.yaml" <<END
  > directory: .
  > ui:
  >   color: no
  > pluginpath:
  >   - $TESTDIR/beetsplug
  > plugins: mockedcandidate importinspect
  > END

Test initial import confirmation on apply

  $ output="$( (echo a; echo y;) | beet import -CWa -S mocked "$TESTDIR/data/250-milliseconds-of-silence.mp3" )"
  $ echo "$output" | grep -F "album: Blank Audio -> An Album"
    album: Blank Audio -> An Album
  $ echo "$output" | grep -F "title: 250 Milliseconds of Silence -> A Track"
    title: 250 Milliseconds of Silence -> A Track




Set up library again to test re-import

  $ rm library.db
  $ beet import -qCWA "$TESTDIR/data/250-milliseconds-of-silence.mp3" >/dev/null 2>&1
  $ beet ls
  Anar Software LLC - Blank Audio - 250 Milliseconds of Silence

Test mocked candidate inspection

  $ output="$( (echo n; echo 1; echo b;) | beet import -L -S mocked id:1 )"
  $ echo "$output" | grep -F "album: Blank Audio -> An Album"
    album: Blank Audio -> An Album
  $ echo "$output" | grep -F "title: 250 Milliseconds of Silence -> A Track"
    title: 250 Milliseconds of Silence -> A Track



Test inspect + confirmation on apply

  $ output="$( (echo a; echo y;) | beet import -L -S mocked id:1 )"
  $ echo "$output" | grep -F "album: Blank Audio -> An Album"
    album: Blank Audio -> An Album
  $ echo "$output" | grep -F "title: 250 Milliseconds of Silence -> A Track"
    title: 250 Milliseconds of Silence -> A Track

