<!--
      Licensed under the Apache License, Version 2.0 (the "License"); you may
      not use this file except in compliance with the License. You may obtain
      a copy of the License at

          http://www.apache.org/licenses/LICENSE-2.0

      Unless required by applicable law or agreed to in writing, software
      distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
      WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
      License for the specific language governing permissions and limitations
      under the License.


      Convention for heading levels in Neutron devref:
      =======  Heading 0 (reserved for the title in a document)
      -------  Heading 1
      ~~~~~~~  Heading 2
      +++++++  Heading 3
      (Avoid deeper levels because they do not render well.)
-->


Getting Started
===============

The information below shows you how to participate in the OpenSwitch Community.

Staying In Touch With the Community
===================================

The best way to reach the OpenSwitch community is through our mailing lists
or on IRC.

Mailing Lists
-------------

The OpenSwitch community uses Google Groups for mailing list communications.
Please subscribe to this mailing list to stay current with discussions around
OpenSwitch development.

IRC
---

OpenSwitch uses [Freenode][4] for IRC. Please join #openswitch.

Sending Your First Patch For Review
===================================

To submit your first patch:

1. To submit patches and develop for OpenSwitch, you must have a [github][1]
account. Please create an account if you do not already have one.
2. Log in to the [OpenSwitch gerrit system][2] using your github account.
3. Add your public SSH key to your account so you can submit patches using
  gerrit-review.
4. Clone the repository you are interested in submitting patches for. A full
  list of repositories can be found at the top of the gerrit system.
5. Create a local branch and make your changes locally.
6. Commit your changes ensuring you use "-s" to git commit. This ensures you
  have the Developers Certificate of Origin ([DCO][5]), which is needed for
  all commits.
7. Push your changes using "git review".

[1]: https://github.com/
[2]: http://review.openswitch.net/
[3]: http://governance.openswitch.net/governance/contributor-onboarding.html#licensing-of-contributions
[4]: http://www.freenode.net/
[5]: http://governance.openswitch.net/governance/contributor-onboarding.html#licensing-of-contributions
