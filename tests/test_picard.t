# Verify that beets works

  $ beet version >/dev/null
  $ echo $?
  0

# Set up initial beets configuration

  $ export BEETSDIR="$PWD"
  $ cat >"$PWD/config.yaml" <<END
  > directory: .
  > ui:
  >   color: no
  > pluginpath:
  >   - $TESTDIR/beetsplug
  > plugins: alias mockedcandidate picard
  > alias:
  >   aliases:
  >     picard: '!echo picard me'
  > END

Set up library

  $ beet import -qCWA "$TESTDIR/data/250-milliseconds-of-silence.mp3" >/dev/null 2>&1

Picard me

  $ beet picard
  picard me
  $ (echo p; echo b;) | beet import -L -S mocked id:1 | sed -n -e '/picard me/s/.*picard/picard/p'
  picard me /.*/data/250-milliseconds-of-silence.mp3 (re)
