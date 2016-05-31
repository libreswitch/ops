# OpenSwitch Project Charter
Effective 2016-05-03
### **1. Mission of the OpenSwitch Project ("OSP").**

- a. create an ecosystem of contributors and users around a full featured network operating system and control plane built to run on Linux enabling the transition to disaggregated networks;
- b. create an open source, open participation technical community to benefit the ecosystem of OSP solution providers and users, focused on network operating system and control plane and management plane use cases that will work across a variety of industry solutions;
- c. promote participation of leading members of the ecosystem, including developers, service and solution providers and end users; and
- d. establish a neutral home for community infrastructure, meetings, events and collaborative discussions and providing structure around the business and technical governance of OSP.

### **2. Membership.**
- a.OSP shall be composed of Premier, General, Operator, and Associate Members. All Premier, General, and Operator Members must be current corporate members of The Linux Foundation (at any level) to participate in OSP as a member. Anyone may propose a contribution to OSP's technical codebase regardless of membership status. All participants in OSP, including Associate Members, enjoy the privileges and undertake the obligations described in this OpenSwitch Project Charter, as from time to time amended by the Governing Board with the approval of The Linux Foundation ("LF"). During the term of their membership, all members will comply with all such policies as the LF Board of Directors and/or the OSP may from time to time adopt with notice to members.
- b.The Associate Member category of membership is limited to non-profits and open source projects, and requires approval by the Governing Board of OSP ("Governing Board"), or, if the Governing Board sets criteria for joining as an Associate Member, the meeting of such criteria. If the Associate Member is a membership organization, Associate Membership in OSP does not confer any benefits or rights to the members of the Associate Member.
- c.The Operator Member category of membership is limited to operators and end users of network switching technologies.  It is not intended for vendors, resellers, or NOS developer organizations.  Membership as an Operator Member requires approval by the Governing Board of OSP ("Governing Board"), or, if the Governing Board sets criteria for joining as an Operator Member, the meeting of such criteria.
- d.Premier Members shall be entitled to appoint a representative to the Governing Board, and to any other committees established by the Governing Board.
- e.General Members shall be entitled to annually elect one representative to the Governing Board for every ten (10) General Members, up to a maximum of three (3) representatives, provided that there shall always be at least one (1) General Member representative, even if there are less than ten (10) General Members. The election process shall be determined by the Governing Board.
- f.Operator Members shall be entitled to annually elect one representative to the Governing Board for every ten (10) Operator Members, up to a maximum of three (3) representatives, provided that there shall always be at least one (1) Operator Member representative, even if there are less than ten (10) Operator Members. The election process shall be determined by the Governing Board.
- g.Premier Members, General Members, Operator Members, and Associate Members shall be entitled to:
	- i.participate in Project general meetings, initiatives, events and related activities; and
	- ii.identify themselves as members of, or participants in, OSP.

### **3. Governing Board**
- a. Composition – the Governing Board voting members shall consist of:
	- i. Up to 16 Premier Members with one representative appointed by each Premier Member;
	- ii. elected General Member representative(s) per Section 2.e.; and
	- iii.Elected Operator Member representative(s) per Section 2.f; and
	- iv. the Chair elected by the Technical Steering Committee, as defined in Section 4 below.
- b. Conduct of Meetings
	- i. Governing Board meetings shall be limited to the Governing Board representatives and follow the requirements for quorum and voting outlined in this Charter. The Governing Board may decide whether to allow one named representative to attend as an alternate.
	- ii. The Governing Board meetings shall be confidential unless approved by the Governing Board. The Governing Board may invite guests to participate in consideration of specific Governing Board topics (but such guest may not participate in any vote on any matter before the Governing Board). The Governing Board should encourage transparency, including the public publication of public minutes within a reasonable time following their approval by the Governing Board.
- c. Responsibilities – the Governing Board shall be responsible for:
	- i. approving a budget directing the use of funds raised by OSP from all sources of revenue;
	- ii. electing a Chair to preside over Governing Board meetings, authorize expenditures approved by the budget and manage any day-to-day operations;
	- iii. verseeing all Project business and marketing matters;
	- iv. adopting and maintaining policies or rules and procedures for OSP (subject to LF approval) including but not limited to a Code of Conduct, a Trademark Policy, and any compliance or certification policies;
	- v. working with the Technical Steering Committee on defining and administering any programs for certification, including any Project certification or processes for OSP;
	- vi. approving procedures for the nomination and election of General and Operator Member representatives to the Governing Board;
	- vii. approving procedures for the nomination and election of any officer or other positions created by the Governing Board;
	- viii. approving the creation and continued existence of any subcommittees or any advisory boards, including their membership, processes for membership, and deliverables; and
	- ix. voting on all decisions or matters coming before the Governing Board.

### **4. Technical Steering Committee ("TSC")**
- a. Composition
	- i. Startup Period: During the first six (6) months after project launch, the TSC voting members shall consist of one (1) appointed representative from each Premier Member, and each current top level project Maintainer, provided that no company (including related companies or affiliates under common control) shall have more than three (3) votes on the TSC.
	- ii. Steady State: After the Startup Period, there shall be a nomination and election period for electing members to the TSC. The TSC voting members shall consist of eleven (11) elected members chosen by the Active Contributors. An Active Contributor is defined as any Contributor who has had a contribution accepted into the codebase during the prior twelve (12) months. Each TSC member must be an Active Contributor or a Maintainer. The election process shall be the Condorcet/Schulze method.  The TSC shall approve the process and timing for nominations and elections held on an annual basis.
- b. TSC projects generally will involve Contributors, Approvers, and Maintainers:
	- i. Contributor: anyone in the technical community that contributes code, documentation or other technical artifacts to the OSP codebase.
	- ii. Approver: A Contributor who has the ability to approve code contributions and reviews in a project's code review and CI/CD infrastructure.
	- iii. Maintainer: A Contributor who is responsible for technical architecture, design, and quality for a project.   Maintainers are expected to cooperate closely with other Maintainers, and with Contributors, with Approvers, and with the TSC and the OSP as a whole.  Maintainers also have the ability to directly commit or merge code and contributions to a project's main branch.  Generally, committing or merging code or contributions outside the control of the code review and CI/CD infrastructure should be rarely done, and carefully deliberated.
	- iv. Participation in OSP through becoming a Contributor and/or Approver and/or Maintainer is open to anyone. The TSC may:
	- * 1.Establish work flows and procedures for the submission, approval and closure or archiving of projects;
	- * 2.Establish criteria and processes for the designation of Approver and Maintainer status; and
	- * 3.Amend, adjust and refine the roles of Contributors, Approvers, and Maintainers, create new roles and publicly document responsibilities and expectations for such roles, as it sees fit.
- c. The TSC shall elect a TSC Chair, who will also serve as a voting member of the Governing Board, and is expected to act as a liaison between the Governing Board and technical leadership of OSP.  The election process for the TSC Chair shall be the Condorcet/Schulze method, with the voters being the members of the TSC.
- d. Responsibilities: The TSC is responsible for:
	- i. coordinating the technical direction of OSP;
	- ii. approving project proposals (including, but not limited to, incubation, deprecation and changes to a project's charter or scope) in accordance with a project lifecycle document to be developed, approved and maintained by the TSC;
	- iii. creating sub-committees or working groups to focus on cross-project technical issues or opportunities;
	- iv. coordinate technical community engagement on requirements, architecture, implementation, use cases, etc.;
	- v. communicating with external and industry organizations concerning Project technical matters;
	- vi. appointing representatives to work with other open source, technical, industry, and standards communities and organizations;
	- vii. establishing community norms, workflows, and policies for releases;
	- viii. discussing, seeking consensus, and where necessary, voting on technical matters relating to the code base that affect multiple projects; and
	- ix. establishing election processes for leadership roles in the technical community that are not within the scope of any single project.
	- x. The election and voting processes for voting on technical matters and electing leadership roles shall be the Condorcet/Schulze method.

### **5. Marketing Committee**
- a. Composition: the Marketing Committee shall consist of:
	- one appointed voting representative from each Premier Member;
	- one non-voting representative appointed by members from other classes of membership; and
	- a non-voting Maintainer appointed by the TSC, if the TSC chooses to appoint a representative.
b - Responsibilities: The Marketing Committee shall be responsible for designing, developing and executing marketing efforts on behalf of the Governing Board. The Marketing Committee is expected to coordinate closely with the Governing Board and with other communities to maximize the outreach and visibility of OSP throughout the industry.

### **6. Voting.  ** It is the goal of OSP to operate as a consensus based community **.**

- a. Election to the positions to the TSC Chair, and to membership on the TSC, and for any decision that the TSC decides is to be decided by a vote, shall be the Condorcet/Schulze method.
- b. If any other decision requires a vote to move forward, the representatives of the Governing Board or Marketing Committee, as applicable, shall vote on a one vote per voting representative basis.
- c. Quorum for Governing Board, Technical Steering Committee, and Marketing Committee meetings shall require two-thirds of the voting representatives. The Governing Board, Technical Steering Committee, or Marketing Committee may continue to meet if quorum is not met, but shall be prevented from making any decisions at the meeting.
- d. Except as provided in Section 6.a, decisions by vote at a meeting shall require a majority vote, provided quorum is met. Decisions by electronic vote without a meeting shall require a majority of all voting representatives.
- e. In the event of a tied vote with respect to an action that cannot be resolved by the Governing Board, the chair shall be entitled to refer the matter to the LF for assistance in reaching a decision. For all decisions in the TSC, Marketing Committee or other committee created by the Governing Board, if there is a tie vote, the matter shall be referred to the Governing Board.

### **7. Antitrust Guidelines**

- a. All members shall abide by The Linux Foundation Antitrust Policy available at http://www.linuxfoundation.org/antitrust-policy.
- b. All members shall encourage open participation from any organization able to meet the membership requirements, regardless of competitive interests. Put another way, the Governing Board shall not seek to exclude any member based on any criteria, requirements or reasons other than those that are reasonable and applied on a non-discriminatory basis to all members.

### **8. Code of Conduct**
- a.The Governing Board shall adopt a Code of Conduct, with approval from the LF.

### **9. Budget**
- a. The Governing Board shall approve an annual budget and never commit to spend in excess of funds raised. The budget and the purposes to which it is applied shall be consistent with the non-profit mission of The Linux Foundation.
- b. The Linux Foundation shall provide the Governing Board with regular reports of spend levels against the budget. In no event will The Linux Foundation have any obligation to undertake any action on behalf of OSP or otherwise related to OSP that will not be covered in full by funds raised by OSP.
- c. In the event any unbudgeted or otherwise unfunded obligation arises related to OSP, The Linux Foundation will coordinate with the Governing Board to address gap funding requirements.

### **10. General & Administrative Expenses**
- a. The Linux Foundation shall have custody of and final authority over the usage of any fees, funds and other cash receipts.
- b. A General & Administrative (G&A) fee will be applied by the Linux Foundation to funds raised to cover Finance, Accounting, and operations. The G&A fee shall equal 9% of OSP's first $1,000,000 of gross receipts and 6% of OSP's gross receipts over $1,000,000.
- c. Under no circumstances shall The Linux Foundation be expected or required to undertake any action on behalf of OSP that is inconsistent with the tax exempt purpose of The Linux Foundation.

### **11. General Rules and Operations.** The OSP project shall be conducted so as to:
- a. engage in the work of the project in a professional manner consistent with maintaining a cohesive community, while also maintaining the goodwill and esteem of The Linux Foundation in the open source software community;
- b. respect the rights of all trademark owners, including any branding and usage guidelines;
- c. engage The Linux Foundation for all OSP press and analyst relations activities;
- d. upon request, provide information regarding Project participation, including information regarding attendance at Project-sponsored events, to The Linux Foundation;
- e. coordinate with The Linux Foundation in relation to any websites created directly for OSP; and
- f. operate under such rules and procedures as may from time to time be approved by the Governing Board and confirmed by The Linux Foundation.

###   **12. Intellectual Property Policy**
- a. Members agree that all new inbound code contributions to OSP shall be made under the Apache License, Version 2.0 (available at [http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)). All contributions shall be accompanied by a Developer Certificate of Origin sign-off ( [http://developercertificate.org](http://developercertificate.org)) that is submitted through a Governing Board and LF-approved contribution process. All contributions by Member employees will bind their employers in accordance with this policy, including the patent and copyright license grants in the Apache License, Version 2.0. Such contribution process will include steps to also bind non-Member Contributors and, if not self-employed, their employer, to the licenses expressly granted in the Apache License, Version 2.0 with respect to such contribution.
- b. All outbound code will be made available under the Apache License, Version 2.0.
- c. All documentation will be contributed to and made available by OSP under the Creative Commons Attribution 4.0 International License (available at http://creativecommons.org/licenses/by/4.0/).
- d.For any new project source code, if an alternative inbound or outbound license is required for compliance with the license for a leveraged open source project or is otherwise required to achieve OSP's mission, the Governing Board may approve the use of an alternative license for specific inbound or outbound contributions on an exception basis. Any exceptions must be approved by a two-thirds vote of the entire Governing Board and the LF and must be limited in scope to what is required for such purpose.
- e. Subject to available Project funds, OSP may engage the LF to determine the availability of, and register, trademarks, service marks, and certification marks, which shall be owned by the LF.

### ** 13. Amendments**
- a.This Charter may be amended by a two-thirds vote of the entire Governing Board, subject to approval by The Linux Foundation.
