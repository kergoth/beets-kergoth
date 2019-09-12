# Verify that beets works

  $ beet version >/dev/null
  $ echo $?
  0

# Set up initial beets configuration

  $ export BEETSDIR="$PWD"
  $ cat >"$PWD/config.yaml" <<END
  > directory: .
  > plugins: alias
  > alias:
  >   aliases:
  >     ls-id: ls -f '\$id'
  >     external: '!echo foo'
  >     'false': '!false'
  >     with-help:
  >       command: '!echo with help'
  >       help: get some help
  > END

List aliases

  $ beet alias
  external: !echo foo
  false: !false
  ls-id: ls -f '$id'
  with-help: !echo with help

Test internal alias

  $ beet import -qCWA "$TESTDIR/data/250-milliseconds-of-silence.mp3" >/dev/null 2>&1
  $ beet -v ls-id 2>&1 | grep 'alias:'
  alias: Running ls -f $id
  $ beet ls-id
  1
  $ beet ls-id -f '$title'
  250 Milliseconds of Silence

Test external alias

  $ beet external -v bar
  foo -v bar

Test alias from path

  $ mkdir bin
  $ cat >bin/beet-test-from-path <<END
  > #!/bin/sh
  > echo testing from path "\$@"
  > END
  $ chmod +x bin/beet-test-from-path
  $ PATH="$PWD/bin:$PATH" beet test-from-path foobar
  testing from path foobar

Test exit code

  $ beet false
  [1]

Test command with help text specified

  $ beet help|grep with-help
    with-help         get some help
  $ beet help with-help
  Usage: beet with-help [options]

  get some help

  $ beet with-help
  with help
