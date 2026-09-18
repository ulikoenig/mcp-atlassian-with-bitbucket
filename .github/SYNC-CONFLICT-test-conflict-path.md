# Manual sync needed: example/fake-upstream

New commits on https://github.com/example/fake-upstream/commit/deadbeef1234567890deadbeef1234567890 (branch `main`) could not be merged into `main` automatically.

Resolve manually, e.g.:

```
git fetch https://github.com/example/fake-upstream.git main
git merge FETCH_HEAD
```

Once resolved on `main`, delete this file and close this PR.
