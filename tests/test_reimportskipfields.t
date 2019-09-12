# Verify that beets works

  $ beet version >/dev/null
  $ echo $?
  0

# Set up initial beets configuration

  $ export BEETSDIR="$PWD"
  $ cat >"$PWD/config.yaml" <<END
  > directory: .
  > import:
  >   quiet_fallback: skip
  > END

Set up initial library

  $ beet import -qCWA "$TESTDIR/data/250-milliseconds-of-silence.mp3" >/dev/null 2>&1
  $ beet ls -f '$id'
  1

Reimport and confirm our set fields are not applied due to skip

  $ beet import -qL --set=reimported=1 id:1 >/dev/null
  $ beet ls -f '$reimported' id:1
  $reimported

Run the same reimport with reimportedskipfields used

  $ cat >>"$PWD/config.yaml" <<END
  > plugins: reimportskipfields
  > reimportskipfields:
  >   set_fields: reimported
  > END
  $ beet import -qL --set=reimported=1 id:1 >/dev/null

Confirm that the field was applied to the skipped item

  $ beet ls -f '$reimported' id:1
  1
