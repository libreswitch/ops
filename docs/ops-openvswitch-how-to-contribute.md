# Contribuiting to Open vSwitch inside OpenSwitch
---

This document describes the workflow for contributing to the ops-openvswitch
module.

# Table of Contents

- [Open vSwitch module structure](#open-vswitch-module-structure)
- [Adding new functionality](#adding-new-functionality)
    - [Creating a feature branch](#creating-a-feature-branch)
    - [Develop the feature](#develop-the-feature)
    - [Publish the feature](#publish-the-feature)
    - [Review process](#review-process)
    - [New Patch creation](#new-patch-creation)
        - [Instructions for the module maintainers](#instructions-for-the-module-maintainers)
- [Updating an existing patch](#updating-an-existing-patch)
    - [Set up the branch](#set-up-the-branch)
    - [Do the fix](#do-the-fix)
    - [Publish the fix](#publish-the-fix)
    - [Review process](#review-process)
    - [Patch file creation](#patch-file-creation)
        - [Instructions for the module maintainers](#instructions-for-the-module-maintainers)

# Open vSwitch module structure
---

Open vSwitch (OVS) module is built in OpenSwitch (OPS) by downloading its
sources directly from [github.com/openvswitch/ovs](
https://github.com/openvswitch/ovs). OPS specific changes are applied as a
collection of patches on top of the OVS code.

The recipe of the module contains the list of patches that are applied to the
OVS code after it is downloaded. Both, the recipe and patch files, reside on
the [openswitch/ops-build](
http://git.openswitch.net/cgit/openswitch/ops-build/tree/yocto/openswitch/meta-distro-openswitch/recipes-ops/openvswitch)
repository. This repository contains all the information necessary to recreate any OVS
build.

Since reviewing the code directly in the patch files can be difficult as the
changes are displayed without the full context of the file, the patch changes
are kept and reviewed in the [openswitch/ovs](
http://git.openswitch.net/cgit/openswitch/ovs) git repository. Note that
this repository exists for the sole purpose of reviewing the code of the
patches. It is neither part of the build process, tested, nor integrated with
CIT.

The openswitch/ovs repository inherits the branches from the OVS project. It has
branches for each release. For example 2.5, the current release, is a branch
named `feature/branch-2.5`. openswitch/ovs has special branches associated with
each release that follow the name convention: `patches/branch-<OVS_VERSION>`. It
contains all the patches that are applied to that particular OVS version in OPS.

Having all the patches applied one after the other on a branch, reduces the
possibility of conflicts between the patch files. Adding new functionality is
easy as it only requires to put a new commit on top of the corresponding patches
branch and generate the new patch file. Also, fixing a bug or updating an
existing patch is also easy as it requires only to update the commit that
generated the patch and then generate a new patch file. The workflow to do this
is described on this document.

This approach keeps the OVS code unchanged in openvswitch/ovs master branch, so
that the repository in OPS is not a fork but a clone, allowing the OPS
community to easily update the OVS version to get bug fixes and new features.
Contributing to the OVS project is also seamless as individual patches can be
sent for upstreaming and then removed once they are part of the OVS code base.

# Setting up openswitch/ovs

Clone the repository in your workspace:
```
git clone https://git.openswitch.net/openswitch/ovs
```

Remember that this repository is only for creating, reviewing, and maintaining
the patches.

# Adding new functionality
---

New functionality can be added on a feature branch. On this branch, the
feature can be split in several commits. This is specially useful for big
changes. The decision of publishing the feature branch falls on to the
developers.

## Creating a feature branch

First, it is necessary to identify which version of OVS is going to be used for
the patch. OVS naming convention for branches names the branches after the
release version. For example the branch for version 2.5 is `feature/branch-2.5`.
Its corresponding patch branch would be `patches/branch-2.5`

Create a new feature branch based on `patches/branch-<OVS_VERSION>`:
```
git checkout --track -b feature/<FEATURE_NAME> patches/branch-<OVS_VERSION>
```
If the branch wants to be published:
```
git push -u gerrit feature/<FEATURE_NAME>
```

## Develop the feature

There are not any special requirement or workflow for the feature branches.
Depending on the size of the feature or the preferences of the developers, the
feature under development could span over several commits. Each commit, as any
in OpenSwitch, needs to go through a Gerrit review before merging.

The code in the feature branch can be reviewed by the developers working in the
new feature. Once it is ready, it needs to be applied in the
`patches/branch-<OVS_VERSION>` branch and the module recipe needs to be updated
to use the new patch.

## Publish the feature

Once the code is ready in the feature branch, it needs to be moved to the
`patches/branch-<OVS_VERSION>` branch as a single commit. First checkout the
branch where the new feature will be applied.
```
git checkout patches/branch-<OVS_VERSION>
```

To avoid having a feature split over several patch files, bring the changes from
`feature/<FEATURE_NAME>` and combined them:
```
git merge --squash  feature/<FEATURE_NAME> # Brings the feature code combined
git commit --signoff # Commit all the changes from the feature branch
```

## Review process

The commit that includes the code in the patches branch needs to be approved by
the module maintainers. To create a new code review issue the command:
```
git review -i patches/branch-<OVS_VERSION>
```

## New Patch creation

Once the maintainers approve the review they will take care of creating the
new patch file and apply it to the recipe.

### Instructions for the module maintainers

The git format-patch option needs to be used in order to keep the commit
information (subject, body, author) as part of the patch. From branch
`patches/branch-<OVS_VERSION>` issue:
```
git format-patch -N HEAD^
```

This will generate a new patch for your commit.

In the openswitch/ops-build repo go to the directory of the ops-openvswitch
recipe:
```
cd yocto/recipes/openswitch/meta-distro-openswitch/recipes-ops/openvswitch/
```

To get the list of all patches issue:
```
ls ops-openvswitch/*.patches
```

Update the numeration in the your patch file so it becomes the last of all.
Copy the new patch to `ops-openvswitch/` directory and include it in the recipe
by adding it to the list of patches in the file `ops-openvswitch.bb`.

Finally, create a review in openswitch/ops-build adding the new patch file and
updating the recipe.

# Updating an existing patch
---

Depending on the size of the change, it can be coded directly on the
`patches/branch-<OVS_VERSION>` branch, or on a feature branch.

## Set up the branch

Checkout the feature branch for the patch if it already exists, or create it if
it does not.
```
// if it already exists, then move to it
git checkout --track -b feature/<FEATURE_NAME>

// if it does not exists, then create it
git checkout --track -b feature/<FEATURE_NAME> patches/branch-<OVS_VERSION>
```

## Do the fix

Do your changes an commit on top of the branch. There are not any special
requirement to do this.

The code in the feature branch can be reviewed by the developers working in the
new feature. Once it is ready, it needs to be applied in the
`patches/branch-<OVS_VERSION>` branch and the module recipe needs to be updated
to use the new patch.

## Publish the fix

Once the fix or refactor is ready in the feature branch, the code needs to be
applied in the `patches/branch-<OVS_VERSION>` branch as a single commit. First,
checkout the branch where the fix will be applied on.
```
git checkout patches/branch-<OVS_VERSION>
```

Bring all the changes from the feature branch and combine them:
```
git merge --squash  feature/<FEATURE_NAME> # Brings the fix code combined
```

This brings the changes from all the commits that were done to do the fix on the
feature branch to the stage of the current branch. Commit them using:
```
git commit --signoff # Creates a commit with all the changes from the feature branch
```

## Review process

As this commit clearly present the changes that are being submitted, this is the
commit that has to be the sent for review to the module maintainers.

To do so issue:
```
git review -i patches/branch-<OVS_VERSION>
```

## Patch file creation

When a fix related to an existing patch is accepted on
`patches/branch-<OVS_VERSION>`, the module maintainers are responsible of
updating the patch list to include the new change.

### Instructions for the module maintainers

To combine two patches use git's rebase functionality. The openswitch/ovs
repository is configured to support the workflow described in this section.

From the `patches/branch-<OVS_VERSION>`, locate the hash of the commit that is
going to be updated. This can be easily done using grep with the name of the
patch file:
```
git log --online | grep <PATCH_NAME>
```

Rebase and combine the changes
```
git rebase -i <HASH_OF_COMMIT_TO_BE_CHANGED>^
```

This puts you in the editor. Move the line with the fix below the commits that
is going to be updated. Then change 'pick' to 'fixup' and save the file.
Conflicts between the commit that was rebased and the old commits will pop out
here. Solve any conflict and continue the rebase until it is done:
```
git rebase --continue
```

Now that the branch history has been rewritten, the branch has to be published
on the remote. To do this, it is necessary to use the --force option as it is
effectively overwriting commits that were already on the remote branch.
```
git push --force origin HEAD:refs/heads/patches/branch-<OVS_VERSION>
```

To generate the new patch the git format-patch option needs to be used in order
to keep the commit information (subject, body, author) as part of the patch and
to keep an standard format for all the patches.

From branch `patches/branch-<OVS_VERSION>` issue:
```
git format-patch -N feature/branch-<OVS_VERSION>
```

This will regenerate the patches of all the commits in the patches branch.
```
cd yocto/recipes/openswitch/meta-distro-openswitch/recipes-ops/openvswitch/
```

Copy the patches to the directory `ops-openvswitch`.  Do not change the patch
names.
Only the patches that were changed need to be copied.

NOTE: we are working on a tool to detected the patches that changed.

Finally, create a review in openswitch/ops-build updating the patch files that
changed.
