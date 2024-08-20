# Verify that beets works

# Set up initial beets configuration

  $ export BEETSDIR="$PWD"
  $ beet version >/dev/null

  $ cat >"$PWD/config.yaml" <<END
  > directory: .
  > plugins: alias
  > alias:
  >   from_path: no
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

Test exit code

  $ beet false
  [1]
  $ beet -v false 2>&1 | grep 'alias:'
  alias: Running false
  alias: command `false` failed with 1

Test command with help text specified

  $ beet with-help
  with help

  $ beet help|grep with-help
    with-help  *get some help (re)

Test alias from path

  $ mkdir bin
  $ cat >bin/beet-test-from-path <<END
  > #!/bin/sh
  > echo testing from path "\$@"
  > END
  $ chmod +x bin/beet-test-from-path
  $ cat >>config.yaml <<END
  > alias:
  >   from_path: yes
  > END
  $ PATH="$PWD/bin:$PATH" beet test-from-path foobar
  testing from path foobar
