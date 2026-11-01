# Fedora downstream packaging

This fork retains upstream NextKDE source, history and attribution. Downstream
RPM recipes, reviewed patches and source checksums live in `.copr/`.
The target is [mcc45tr/kdenext](https://copr.fedorainfracloud.org/coprs/mcc45tr/kdenext/),
**Fedora Rawhide AArch64 only**. Fedora's original Plasma and KDE applications
are used without creating Uke variants.

2026-11-01: all 18 runtime and meta packages built on native Rawhide AArch64.
Upstream Settings, Go, KMusic, NkMail and ListenFree build-VM checks passed. Source,
COPR build, package checks and physical-device acceptance are separate results.
No installation or graphical-session qualification is claimed here.

## Source and package scope

| Source | Pin | Package scope |
| --- | --- | --- |
| NextKDE | v0.1.1, `2ca59a1fbe7cd8c4b9c0b9fd960edca6788425c5` | Desktop, Settings, KWin effects/decoration and native QML plugins, data/PIM services, Calculator, Calendar, Todo, Weather, legacy Music, spatial worker/mesh and login/lock themes |
| ListenFree in NextKDE | Same release, application 0.3.8 | Player and its exact patched Qmmp 2.4.1, QuickJS-ng 0.16.2 and TagLib 2.3.1 sources |
| Quickshell | v0.3.2, `4f508be500dea6e5732cc3d50382a0048b17e7b1` | Desktop toolkit required by the shell |
| KMusic | `ad0222d4404a166a1607e2967f3201cea64111c5` | Independent music application, exact vendored Kos.Ui and provider sources |
| NkMail | `483a664317cd1efa43b10ae6d461caa53182ce30` | Independent mail application and its patched mailio 0.26.1 |
| NkMail Kos.Ui | Recorded gitlink `e2592b2742c58c1bd797a8bcfa2a3ae7da4affd8` | Canonical UI sources compiled into NkMail; no moving submodule branch |

`nextkde-full` selects the complete packaged main release. `nextkde-suite` also
selects the independent KMusic and NkMail applications and the original Fedora
Plasma desktop, Dolphin, Konsole, System Settings and desktop portal. Components can be
installed independently. The legacy KOS Music player and ListenFree coexist;
the RPM does not migrate user data or change media associations. Upstream's
per-user installers are not run by the package.

The spatial engine uses Fedora ONNX Runtime and OpenCV. Model weights remain
upstream's explicitly enabled, checksum-verified user-cache downloads; they are
not bundled. Theme packages do not select a login manager or lock screen.
User services and KOS effects are not enabled automatically.

The KWin plugins require KWin 6.8.2; Qt private API requirements also constrain
Quickshell. Rebuild and validate the packages when those ABI versions change.
The optional Quickshell crash handler remains disabled because Fedora cpptrace
lacks the required signal-safe unwinding support.

## Install the complete desktop

```sh
sudo dnf copr enable mcc45tr/kdenext
sudo dnf install nextkde-suite
```

These commands were not executed on the host. The metapackage supplies all
runtime components; activation of the shell, login and lock themes remains an
explicit user choice. Rawhide KWin and Qt ABI updates can require rebuilding.

## Build and publish

Install Fedora source-build tools (`rpm-build`, `redhat-rpm-config`, Go 1.26+,
`curl`, `tar`, `git` and `copr-cli`), then run:

```sh
bash .copr/build-srpms.sh
copr-cli build --nowait --enable-net off -r fedora-rawhide-aarch64 \
  mcc45tr/kdenext .copr/build/rpmbuild/SRPMS/*.src.rpm
```

Sources are verified against `sources.tsv` before extraction. Go dependencies
are generated from the pinned module files and verified during SRPM
preparation. Binary builds run without network access. Generated archives,
build output and private receipts are ignored by Git.

Pass one source package name to build only its SRPM, for example
`bash .copr/build-srpms.sh nextkde-suite`. Source preparation explicitly targets
AArch64 and can run on a different build-host architecture; the binary COPR
build remains native AArch64. COPR package source jobs fetch this fork and use
the same helper instead of depending on a temporary uploaded SRPM URL.

NkMail's unmodified upstream Python CLI and loopback-protocol test fixtures
run only inside the COPR build VM, pinned by its full source commit. Reusing
those fixtures preserves their TLS/error-path coverage. Python source or a
Python runtime is not installed by these application RPMs. Unmodified Fedora
dependencies retain their own distribution helpers.

## Upstream maintenance

The daily `Fedora upstream sync` workflow merges `NextKde/NextKde:main` into this
fork's `main`. It preserves downstream commits and never force-pushes. A
conflict aborts without changing the remote branch. The workflow is also
available manually; its merge/conflict test runs before synchronization.

RPM sources remain pinned to tested revisions. Daily source synchronization
does not silently promote an untested upstream snapshot into COPR. To update a
package, change its source pin and checksum, refresh the applicable patch,
build all affected RPMs, run package/dependency checks and update this record.

Device adjustments belong in reviewed patches under `.copr/patches/`. Keep
them separate from generic Fedora paths and default them to explicit user
selection. A package or build result does not establish device behavior.
