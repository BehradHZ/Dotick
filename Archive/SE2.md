# مجموعه PDFهای تبدیل‌شده

تعداد کل PDFها: 11

تعداد تبدیل موفق: 11

تعداد تبدیل ناموفق: 0



---

# سند 1: 01_NatureOfSoftware

**فایل اصلی:** `01_NatureOfSoftware.pdf`

# **The Nature of Software & Software Engineering**

## ■ **Chapters 1 & 2**

*Slide Set to accompany*

*Software Engineering: A Practitioner's Approach, 8/e*

**by Roger S. Pressman and Bruce R. Maxim**

**Slides copyright © 1996, 2001, 2005, 2009, 2014 by Roger S. Pressman**

#### *For non-profit educational use only*

May be reproduced ONLY for student use at the university level when used in conjunction with *Software Engineering: A Practitioner's Approach, 8/e.* Any other reproduction or use is prohibited without the express written permission of the author.

All copyright information MUST appear if these slides are posted on a website for student use.

## Agenda

- The Nature of Software
- Software Engineering

![](01_NatureOfSoftware/01_NatureOfSoftware/_page_1_Picture_3.jpeg)

# *The Nature of Software*

## What is Software?

#### Software is:

- (1) **instructions** (computer programs) that when executed provide desired features, function, and performance;
- (2) **data structures** that enable the programs to adequately manipulate information and (3) **documentation** that describes the operation and use of the programs.

## The Nature of Software

- Software is developed or engineered, it is not manufactured in the classical sense.
- Software is a logical rather than a physical element.
- Software doesn't "wear out."
  - wear out:

![](01_NatureOfSoftware/01_NatureOfSoftware/_page_4_Picture_5.jpeg)

- Software deteriorates
- Deteriorate = become progressively worse

## Failure Curve for Hardware

![](01_NatureOfSoftware/01_NatureOfSoftware/_page_5_Figure_1.jpeg)

These slides are designed to accompany *Software Engineering: A Practitioner's Approach, 8/e* (McGraw-Hill 2014). Slides copyright 2014 by Roger Pressman. 6

## Wear vs. Deterioration

![](01_NatureOfSoftware/01_NatureOfSoftware/_page_6_Picture_1.jpeg)

## Software Changes

- What may change in a software, and why?
  - Requirements
    - Technical requirements
    - Business requirements
  - Analysis & Design
  - Implementation

## Software Application Domains

- System software
  - Programs that service other programs (OS, drivers, compilers)
- Application software
- Engineering/Scientific software
- Embedded software
- Product-line software
- Web/Mobile applications
- AI software (robotics, neural nets, game playing)

Hybrid Categories

## Legacy Software

- Those old programs
- Developed decades ago
- Have been continually modified to meet changes
- Headaches for large organization:
  - They are costly to maintain and risky to evolve
- But they are critical for the business
  - Many legacy systems remain supportive to core business functions and are '**indispensable**' to the business
- Often with poor quality
  - Inextensible designs, convoluted code
  - Lack of documentation, test cases and results
  - Poorly managed change history

![](01_NatureOfSoftware/01_NatureOfSoftware/_page_9_Picture_12.jpeg)

## Legacy Software (cont.)

- What to do?
  - The only reasonable answer is:
  - Do nothing,
  - At least until the legacy system must undergo some **significant** change
    - Software must be re-engineered to make it viable within a evolving environment

## New Trends

- WebApps
  - Internet-based, Unpredictable load, Performance, Availability, …
- Mobile Apps
- Cloud Computing
- Product Line Software

## Cloud Computing

■ *Cloud computing* encompasses an infrastructure or "ecosystem" that enables any user, anywhere, to share computing resources using a computing device

![](01_NatureOfSoftware/01_NatureOfSoftware/_page_12_Figure_2.jpeg)

## Cloud Computing (cont.)

- Provides distributed storage and processing resources to different computing devices
- Computing devices reside outside the cloud and have access to a variety of resources inside the cloud
  - Applications, platforms, and infrastructure
- In its simplest form, an external computing device accesses the cloud via a Web browser or analogous software
- The cloud provides access to data that resides with databases and other data structures
- In addition, devices can access executable applications that can be used in lieu of apps that reside on the computing device
- Requires developing an architecture containing both frontend and backend services

## Cloud Computing (cont.)

- Frontend services include the client (user) devices and application software (e.g., a browser) that allows the back-end to be accessed
- Backend services include servers, data storage (e.g., databases), and server-resident applications
- Cloud architectures can be segmented to provide access at a variety of different levels
  - From full public access to private cloud architectures accessible only to those with authorization

# *Software Engineering*

# Why Software Engineering?

### Some realities:

- *A concerted effort should be made to understand the problem before a software solution is developed*
- *Design becomes a pivotal activity*
- *Software should exhibit high quality*
- *Software should be maintainable*

## Conclusion:

 Software in all of its forms and across all of its application domains should be engineered

# What is Software Engineering?

- The IEEE definition:
  - *Software Engineering:*
  - *(1) The application of a systematic, disciplined, quantifiable approach to the development, operation, and maintenance of software; that is, the application of engineering to software.*
  - *(2) The study of approaches as in (1)*

# Software Engineering: A Layered Technology

![](01_NatureOfSoftware/01_NatureOfSoftware/_page_18_Picture_1.jpeg)

*Software Engineering*

![](01_NatureOfSoftware/01_NatureOfSoftware/_page_19_Picture_0.jpeg)

# Layered Technology

### **Quality** Layer

- An organizational commitment to quality
  - A continuous improvement culture

### **Process** Layer

- The foundation for software engineering
- Defines a framework that must be established for effective delivery of software
- It forms the basis for:
  - project management, producing work products, achieving milestones, quality assurance and change management
- Example?

![](01_NatureOfSoftware/01_NatureOfSoftware/_page_20_Picture_0.jpeg)

# Layered Technology (cont.)

### **Methods** Layer

- Provides the technical how-to's for building software
- Methods include techniques of:
  - communication, requirements analysis, design, program construction, testing, and support

## **Tools** Layer

- Provides automated or semi-automated support for the process and methods
- Computer-Aided Software Engineering (CASE)
- Example?
  - Management, Documentation, Design, Versioning, Test,…

## Hooker's General Principles

- 1: *The Reason It All Exists*
- 2: *KISS (Keep It Simple, Stupid!)*
- 3: *Maintain the Vision*
- 4: *What You Produce, Others Will Consume*
- 5: *Be Open to the Future*
- 6: *Plan Ahead for Reuse*
- 7*: Think!*

*If every software engineer and every software team simply followed Hooker's seven principles, many of the difficulties we experience in building complex computer-based systems would be eliminated*

## 1) The Reason It All Exists

- A software system exists for **one reason**: to provide value to its users
- All decisions should be made with this in mind
- Before specifying a system requirement, before determining the hardware platforms or development processes,
  - Ask yourself questions such as:
    - "Does this add real VALUE to the system?"
  - If the answer is
    - "No"
  - **Don't** do it
- All other principles support this one

# 2) KISS (Keep It Simple, Stupid!)

- All design should be as simple as possible, **but no simpler**
- The more elegant designs are usually the more simple ones
- This facilitates having a more easily understood, and easily maintained system
- This is not to say that features should be discarded in the name of simplicity
- Simple also does not mean "quick and dirty"
- In fact, it often takes a lot of thought and work over multiple iterations to simplify
- The payoff is software that is more maintainable and less error-prone

## 3) Maintain the Vision

- A clear vision is essential to the success of a software project
- Without one, a system threatens to become a patchwork of incompatible designs, held together by the wrong kind of screws
- Having a clean internal structure is essential to constructing a system that is understandable, extendible, maintainable and testable
- Having an empowered Architect who can hold the vision and enforce compliance helps ensure a very successful software project

# 4) What You Produce, Others Will Consume

- Someone else will use, maintain, document, or otherwise depend on being able to understand your system
- So, always specify, design, and implement knowing someone else will have to understand what you are doing
- Specify with an eye to the users
- Design, keeping the implementers in mind
- Code with concern for those that must maintain and extend the system
  - Someone may have to debug the code you write, and that makes them a user of your code
- Making their job easier **adds value to the system**

## 5) Be Open to the Future

- A system with a long lifetime has more value
- Today software lifetimes are typically measured in months instead of years
- True "industrial-strength" software systems must endure far longer
  - These systems must be ready to **adapt** to changes
  - Systems that do this successfully are those that have been designed this way from the start
  - Always ask "what if ", and prepare for all possible answers by creating systems that solve the general problem, not just the specific one
  - This could very possibly lead to the reuse of an entire system

## 6) Plan Ahead for Reuse

- Reuse saves time and effort
- Achieving a high level of reuse is arguably the hardest goal to accomplish in developing a software system
- The reuse of code and designs is a major benefit of using **object-oriented** technologies
- However, the return on this investment requires forethought and planning

## 7) Think!

- This last Principle is probably the most overlooked
- Placing clear, complete thought before action almost always produces better results
- When you think about something, you are more likely to do it right
- You also gain knowledge about how to do it right again
- If you do think about something and still do it wrong, it becomes valuable experience
- Applying the first six Principles requires intense thought

## Software Myths

*Recognition of software realities is the first step toward formulation of practical solutions for software engineering*

- Erroneous beliefs about software and the process
- Misleading attitudes that affect managers, customers and practitioners
- Are believable because they often have elements of truth,

#### *but …*

Invariably lead to bad decisions,

#### *therefore …*

 Insist on reality as you navigate your way through software engineering

## Management myths

*Myth: If we get behind schedule, we can add more programmers and catch up* 

- Software development is not a mechanistic process like manufacturing
- Adding people to a late software project makes it later
- *Myth: If I decide to outsource the software project to a third party, I can just relax and let that firm build it*
- **Reality:** If an organization does not understand how to manage and control software projects internally, it will invariably struggle when it outsources

## Customer myths

- In many cases, the customer believes myths about software because
  - Software managers and practitioners **do little** to correct misinformation.
- Myths lead to false expectations (by the customer)
  - Ultimately, dissatisfaction with the developer

## Customer myths (1)

*Myth: A general statement of objectives is sufficient to begin writing programs—we can fill in the details later*

- A comprehensive and stable statement of requirements is not always possible
- However, an ambiguous "statement of objectives" is a disaster
- Unambiguous requirements (usually derived iteratively) are developed only through:
  - Effective and continuous communication between customer and developer

# Customer myths (2)

*Myth: Software requirements continually change, but change can be easily accommodated because software is flexible*

- The impact of change varies with the time at which it is introduced
- When requirements changes are requested early (before design or code) the cost impact is relatively small
- As time passes, the cost impact grows rapidly
  - Additional resources and major design modification

## Myths fostered by over 60 years of programming culture

# Practitioner's myths (1)

*Myth: Once we write the program and get it to work, our job is done*

- "The sooner you begin 'writing code,' the longer it'll take you to get done."
- Between 60 and 80 percent of all effort expended on software will be expended after its first delivery to customers

# Practitioner's myths (2)

*Myth: Until I get the program "running" I have no way of assessing its quality*

- Technical review
  - One of the most effective software quality assurance mechanisms
  - It can be applied from the inception of a project
  - It is more effective than dynamic testing for finding certain classes of software defects

# Practitioner's myths (3)

*Myth: The only deliverable work product for a successful project is the working program*

- A working program is only one part of a software configuration
- A variety of work products (e.g., models, documents, plans)
  - Foundation for successful engineering
  - Guidance for software support

# Practitioner's myths (4)

- *Myth: Software engineering will make us create voluminous and unnecessary documentation and will invariably slow us down*
  - We have no time!!!

- Software engineering is not about creating documents
- It is about creating a quality product
- Better quality leads to **reduced rework**
  - Reduced rework results in faster delivery times

## Further Reading

Chapters 1 & 2 of Pressman

# *The End*



---

# سند 2: 02_SoftwareProcess

**فایل اصلی:** `02_SoftwareProcess.pdf`

### **The Software Process**

#### **Chapters 3 & 4**

*Slide Set to accompany*

*Software Engineering: A Practitioner's Approach, 8/e*

**by Roger S. Pressman and Bruce R. Maxim**

**Slides copyright © 1996, 2001, 2005, 2009, 2014 by Roger S. Pressman**

#### *For non-profit educational use only*

May be reproduced ONLY for student use at the university level when used in conjunction with *Software Engineering: A Practitioner's Approach, 8/e.* Any other reproduction or use is prohibited without the express written permission of the author.

All copyright information MUST appear if these slides are posted on a website for student use.

## Agenda

- Software Process Structure
- Process Models

![](02_SoftwareProcess/02_SoftwareProcess/_page_1_Picture_3.jpeg)

### *Software Process Structure*

![](02_SoftwareProcess/02_SoftwareProcess/_page_3_Picture_0.jpeg)

### Software Process

 "A process defines *who* is doing *what, when* and *how* **to** reach a certain goal."

> *Ivar Jacobson, Grady Booch, and James Rumbaugh*

- Process defines the approach that is taken as software is engineered
- Framework for **activities**, **actions**, and **tasks**
  - required to build high-quality software

## Activity, Action and Task

- Activity strives to achieve a broad objective
  - Applied **regardless of** the application domain, size of the project, complexity of the effort,...
  - e.g., modeling, communication, …
- Action encompasses a set of tasks that produce a major work product
  - e.g., architectural design (major product: an architectural design model).
- Task focuses on a small, but well-defined objective that produces a tangible outcome
  - e.g., conducting a unit test

### A Generic Process Framework

#### **Process framework Framework activities**

work tasks work products milestones & deliverables QA checkpoints

**Umbrella Activities**

#### Framework Activities VS Umbrella Activities

- Framework activities are applicable to all software projects, regardless of their size or complexity
- Umbrella activities are applicable across the entire software process
  - Complement framework activities
  - Applied throughout a software project

![](02_SoftwareProcess/02_SoftwareProcess/_page_6_Figure_6.jpeg)

These slides are designed to accompany *Software Engineering: A Practitioner's Approach, 8/e*  (McGraw-Hill 2014). Slides copyright 2014 by Roger Pressman. 7

### Framework Activities

#### **Communication**

- Collaborate with the customer and stakeholders
- Intent: to understand objectives and to gather requirements

#### **Planning**

Software project plan (risks, resources, products, schedules,..)

#### **Modeling**

- Analysis of requirements
- Design

#### **Construction**

Code generation and Testing

#### **Deployment**

- The software is delivered to the customer
- The customer evaluates the product and provides feedback

### Notes on Framework Activities

- These five **generic** framework activities can be used for the development of different systems (from small and simple to large and complex)
  - The details of the process is quite different in each case, but the framework activities remain the same
- For many software projects, framework activities are applied iteratively
  - Applied repeatedly through a number of iterations
  - Each iteration produces a software increment
  - An increment provides a subset of overall features
  - Software is gradually completed

## Typical Umbrella Activities

- Software project tracking and control
- Risk management
- Software quality assurance
- Technical reviews
- Measurement
  - e.g., lines of code, code complexity, customer satisfaction score, cycle time, cost variance, schedule variance,…
- Software configuration management
- Reusability management
- Work product preparation and production

### Process Adaptation

- Software process is **not a rigid prescription**
- It should be **adaptable**
  - to the problem,
  - to the project,
  - to the team.
- Conclusion:
  - A process adopted for one project might be significantly different than a process adopted for another project

### Adapting a Process Model

- The overall flow of activities, actions, and tasks and the interdependencies among them
- The degree to which actions and tasks are defined within each framework activity
- The degree to which work products are identified and required
- The manner which quality assurance activities are applied
- The manner in which project tracking and control activities are applied
- The degree to which the customer and other stakeholders are involved with the project
- The level of autonomy given to the software team
- The degree to which team organization and roles are prescribed

## Example: Adapting a Task Set

*Action:* Requirements gathering (an important action during the communication activity)

#### **Task set for a small and simple project**

#### **Task set for a large and complex project**

- 1. Make a list of stakeholders for the project
- 2. Interview each stakeholder separately to determine overall needs
- 3. Build a preliminary list of functions and features based on stakeholder input
- 4. Schedule a series of facilitated application specification meetings
- 5. Conduct meetings
- 6. Produce informal user scenarios as part of each meeting
- 7. Refine user scenarios based on stakeholder feedback
- 8. Build a revised list of stakeholder requirements
- 9. Prioritize requirements

10. ….

13

# Process Flow (also called *work flow*)

![](02_SoftwareProcess/02_SoftwareProcess/_page_13_Figure_1.jpeg)

These slides are designed to accompany *Software Engineering: A Practitioner's Approach, 8/e*  (McGraw-Hill, 2014). Slides copyright 2014 by Roger Pressman. 14

### Linear Flow

**Linear process** flow executes each of the five framework activities in sequence, beginning with communication and culminating with deployment

![](02_SoftwareProcess/02_SoftwareProcess/_page_14_Figure_2.jpeg)

### Iterative Flow

**Iterative process** flow repeats one or more of the activities before proceeding to the next

![](02_SoftwareProcess/02_SoftwareProcess/_page_15_Figure_2.jpeg)

## Evolutionary Flow

- **Evolutionary process** flow iterates the activities in a "circular" manner
- Each circuit through the five activities leads to a more complete version of the software

![](02_SoftwareProcess/02_SoftwareProcess/_page_16_Figure_3.jpeg)

### Parallel Flow

- **Parallel process** flow executes one or more activities in parallel with other activities
- For example, modeling for one aspect of the software might be executed in parallel with construction of another aspect of the software

![](02_SoftwareProcess/02_SoftwareProcess/_page_17_Figure_3.jpeg)

### Process Patterns

- A *process pattern*
  - Describes a **repeatable process-related problem**,
  - Identifies the **environment** in which the problem has been encountered, and
  - Suggests one or more **proven solutions** to the problem.
- Each pattern must include:
  - Pattern name, intent, type, initial context, problem, solution, and resulting context
- Example: Pattern name=RequirementsUnclear
  - Problem: Requirements are hazy or nonexistent
    - stakeholders are unsure of what they want
  - Solution: A description of the prototyping process

### Process Pattern Types

- *Stage patterns*—defines a problem associated with a framework **activity** for the process.
- *Task patterns*—defines a problem associated with a software engineering **action** or work task
- *Phase patterns*—define the **sequence of framework activities** that occur with the process

#### A Sample Process Pattern

These slides are designed to accompany *Software Engineering: A Practitioner's Approach, 8/e* 

## *Process Models*

![](02_SoftwareProcess/02_SoftwareProcess/_page_22_Picture_0.jpeg)

### Process Model

- A specific roadmap for software engineering It defines the flow of all activities, actions and tasks, the degree of iteration, the work products, and the organization of the work that must be done
- Different process models:
  - Traditional models and Agile models
- Different models are suitable for different projects
- Software process model ≈ Software process ≈ software development **methodology** ≈ software development life cycle ≈ software development process

### Prescriptive Models

- Prescriptive process models advocate an orderly approach to software engineering
  - They strive for structure and order in software development
  - Sometimes referred to as "traditional" process models
  - Examples: Waterfall, Spiral,…
- Prescriptive process models define a prescribed set of **process elements** and a predictable **process flow**
  - Process elements: framework activities, actions, tasks, work products, quality assurance, and change control mechanisms
  - They prescribe a process flow (also called work flow)

### The Waterfall Model

![](02_SoftwareProcess/02_SoftwareProcess/_page_24_Figure_1.jpeg)

- The waterfalls model, sometimes called the **classic life cycle**
- A systematic, sequential approach to software development
- The oldest paradigm for software engineering
- A linear process model: progress is flowing steadily downwards (like a waterfall)

### Problems with Waterfall

- 1. Real projects rarely follow the sequential flow that the model proposes
  - After-the-fact changes are prohibitively costly (if not impossible)
- 2. Difficult for the customer to state all requirements explicitly
- 3. The customer must have patience
  - A working version will not available late
  - A major blunder, if undetected until the working program is reviewed, can be disastrous
- 4. "Blocking states" problem

## The Applicability of Waterfall

- When the requirements for a problem are well understood and reasonably stable
- This situation is often encountered when welldefined adaptations or enhancements to an existing system must be made
  - E.g., an adaptation to an accounting software because of changes to government regulations

### The V-Model

- A variation of the waterfall model
  - A variation in the **representation**
  - No fundamental difference
  - V-model is also linear

![](02_SoftwareProcess/02_SoftwareProcess/_page_27_Figure_5.jpeg)

### The Incremental Model

- There are many situations in which initial software requirements are reasonably well defined
- But we need to provide a limited set of software functionality to users quickly
  - Then refine and expand on that functionality in later releases
- In such cases, we choose a process model that is designed to produce the software in increments
  - Combines linear and parallel process flows

### The Incremental Model

![](02_SoftwareProcess/02_SoftwareProcess/_page_29_Figure_1.jpeg)

![](02_SoftwareProcess/02_SoftwareProcess/_page_30_Picture_0.jpeg)

### The Incremental Model

- Each linear sequence produces deliverable "increments" of the software
  - The first increment is often a **core product**
  - Basic requirements are addressed
  - But many supplementary features remain undelivered
- The core product is used by the customer
  - A working version will be available late **sooner**
- Based on evaluation results:
  - A plan is developed for the next increment
  - The core product is modified to better meet the customer needs and the delivery of additional features
- This process is repeated until the product is completed

### Example

- Word-processing software developed using the incremental paradigm:
  - In the **first increment**: deliver basic file management, editing, and document production functions
  - In the **second increment**: more sophisticated editing and document production capabilities
  - In the **third increment**: spelling and grammar checking
  - In the **fourth increment**: advanced page layout capability

![](02_SoftwareProcess/02_SoftwareProcess/_page_32_Picture_0.jpeg)

### Evolutionary Process Models

- Software, like all complex systems, evolves over time
  - Grows and changes
- In these situations, you need an evolutionary model:
  - 1. Business and product requirements often change as development proceeds, making an end product unrealistic
  - 2. A set of basic requirements is well understood, but the details of product are unknown and have yet to be defined (not soon)
- Evolutionary models are **iterative**
- Two common evolutionary models:
  - Prototyping
  - Spiral

### Iterative vs. Incremental?

- An iterative process makes progress through continuous refinement
  - The final product may be quite different from the initial product
- An incremental process makes progress through small

increments

 Releasing small features at a time depending on their priorities

![](02_SoftwareProcess/02_SoftwareProcess/_page_33_Figure_6.jpeg)

# Evolutionary Models: Prototyping

- What is a prototype?
  - An early sample, model, or release of a product
- Benefit?
  - To get valuable **feedback** from the users early in the project
  - To be sure of the efficiency of an algorithm, the adaptability of an operating system, or …
- Better understand what is to be built when requirements are fuzzy
- It can be used within the context of any process model

# Prototyping

- Two kinds of prototypes:
- 1. Throwaways
  - may be too slow, too big, awkward in use or all three
- 2. Evolutionary
  - slowly evolves into the actual system
- The problems of prototyping:
- 1. Stakeholders see what appears to be a working version of the software
- 2. As a software engineer, you often make implementation compromises in order to get a prototype working quickly

![](02_SoftwareProcess/02_SoftwareProcess/_page_35_Picture_9.jpeg)

![](02_SoftwareProcess/02_SoftwareProcess/_page_36_Picture_0.jpeg)

## Evolutionary Models: The Spiral

- Using the spiral model, software is developed in a series of iterations (i.e., evolutionary releases).
- During early iterations, the release might be a model or prototype.
- During later iterations, increasingly more complete versions of the engineered system are produced
- It is a **risk-driven** model
  - Better understand and react to risks
- A realistic approach to the development of largescale systems

![](02_SoftwareProcess/02_SoftwareProcess/_page_36_Picture_8.jpeg)

### Still Other Process Models

- Component based development—the process to apply when *reuse* is a development objective
- Formal methods—emphasizes the *mathematical specification* of requirements
- AOSD—provides a process and methodological approach for defining, specifying, designing, and constructing *aspects*
- Unified Process—a "**use-case driven**, **architecturecentric**, **iterative** and **incremental**" software process closely aligned with the Unified Modeling Language (UML)

![](02_SoftwareProcess/02_SoftwareProcess/_page_37_Picture_5.jpeg)

## Further Reading

| PART ONE  | THE SOFTWARE PROCESS 29                  |
|-----------|------------------------------------------|
| CHAPTER 3 | Software Process Structure 30            |
| CHAPTER 4 | Process Models 40                        |
| CHAPTER 5 | Agile Development 66                     |
| CHAPTER 6 | Human Aspects of Software Engineering 87 |

## *The End*

# *Further Study: Other Process Models*

## Component-Based Development

- The component-based development comprises applications from reusable components
- Commercial off-the-shelf (COTS) software components
  - Developed by vendors
  - Provides targeted functionality with welldefined interfaces that enable the component to be integrated into the software

### The Formal Methods

- Enable you to specify, develop, and verify a software by applying mathematical notation
- They provide a mechanism for eliminating many of the problems that are difficult to overcome using other software engineering paradigms.
  - Ambiguity, incompleteness, and inconsistency can be discovered and corrected more easily—not through ad-hoc review, but through the application of mathematical analysis
- The formal methods approach has gained adherents for safety-critical software systems
  - e.g., aircraft avionics, medical devices, etc.

# Challenges of the Formal Methods

- The development of formal models is currently quite time consuming and expensive
- Few software developers have the necessary background to apply formal methods
  - extensive training is required
- It is difficult to use the models as a communication mechanism for technically unsophisticated customers

# Aspect-Oriented Software Development (AOSD)

- Core concerns vs. Cross-cutting concerns
  - Core concerns: primary functionality of the system (business logic)
    - E.g., place a new order
  - Cross-cutting concerns: concerns that cut across multiple system functions, features, and information

![](02_SoftwareProcess/02_SoftwareProcess/_page_44_Picture_5.jpeg)

### Aspects

- An *aspect* is a representation of a cross-cutting concern.
- Example:
  - Authentication
  - Log
  - …
- Aspects modularize cross-cutting concerns that would otherwise end up scattered across several modules.

![](02_SoftwareProcess/02_SoftwareProcess/_page_45_Picture_7.jpeg)

![](02_SoftwareProcess/02_SoftwareProcess/_page_45_Picture_8.jpeg)

### AOP vs. OOP

![](02_SoftwareProcess/02_SoftwareProcess/_page_46_Picture_1.jpeg)

- AOP is **not a competitor** for OOP
  - it emerged out of OOP paradigm
  - AOP extends OOP by addressing few of its problems
  - AOP introduces neat ways to implement crosscutting concerns in a single place
    - which might have been scattered over several places in the corresponding OOP implementation
  - AOP makes the program cleaner and more loosely coupled
- So, it is **not** AOP **vs** OOP
  - It is AOP **with** OOP

### AOP—An Example

- Note: Everything that AOP does could also be done without it by just adding more code
  - **AOP just saves you writing extra codes**
- Assume you have a graphical class with many "set...()" methods
- After each set method, the data of the graphics changed
  - thus the graphics need to be updated on screen
- Assume to repaint the graphics you must call "Display.update()"
- The classical approach is to solve this by adding *more code*. At the end of each set method you write:

## AOP—An Example (cont.)

- If you have 3 set-methods, that is not a problem
- But if you have 200 (hypothetical), it's getting real painful to add this everywhere
- Also whenever you add a new set-method, you must be sure to not forget adding this to the end
  - otherwise you just created a bug
- AOP solves this without adding tons of code, instead you add **an aspect:**

- And that's it! Instead of writing the update code yourself, you just tell the system that after a set() pointcut has been reached, it must run this code.
  - No need to update 200 methods, no need to make sure you don't forget to add this code on a new set-method

## AOP—An Example (cont.)

Additionally you just need a pointcut:

- That means:
  - if a method is named "set\*" (\* means any name might follow after set),
  - regardless of what the method returns or what parameters it takes
  - and it is a method of MyGraphicsClass
  - and this class is part of the package "com.company.\*",
  - then this is a set() pointcut.
- And our first code (previous slide) says:
  - "after running any method that is a set() pointcut, run the following code.

## AOP—An Example (cont.)

- Everything described in this example **can** be done at compile time.
- The pre-processor of AOP can just modify your source
  - e.g. adding Display.update() to the end of every set-pointcut method, before even compiling the class itself

## *Further Study: Risk Analysis*

## Assessing Project Risk

- Is project scope stable?
- Does the software engineering team have the right mix of skills?
- Are project requirements stable?
- Does the project team have experience with the technology to be implemented?
- Is the number of people on the project team adequate to do the job?
- Do all customer/user constituencies agree on the importance of the project and on the requirements for the system/product to be built?
- …

### Risks Due to the Customer

- **Have you worked with the customer in the past?**
- **Has the customer agreed to spend time with you?**
- **Is the customer willing to participate in reviews?**
- **Is the customer technically sophisticated?**
- **Is the customer willing to let your people do their job—that is, will the customer resist looking over your shoulder during technically detailed work?**
- **Does the customer understand the software engineering process?**

### Risks Due to Process Maturity

- **Have you established a common process framework?**
- **Is it followed by project teams?**
- **Do you have management support for software engineering ?**
- **Do you conduct formal technical reviews?**
- **Are CASE tools used for analysis, design and testing?**

## Technology Risks

- **Is the technology new to your organization?**
- **Are new algorithms, I/O technology required?**
- **Is new or unproven hardware involved?**
- **Does the application interface with new software?**
- **Is a specialized user interface required?**
- **Are you using new software engineering methods?**
- **Are you using unconventional software development methods, such as formal methods, AI-based approaches, artificial neural networks?**

### Staff/People Risks

- **Are the best people available?**
- **Does staff have the right skills?**
- **Are enough people available?**
- **Are staff committed for entire duration?**
- **Will some people work part time?**
- **Do staff have the right expectations?**
- **Have staff received necessary training?**
- **Will turnover among staff be low?**

## Recording Risk Information

**Project: Embedded software for XYZ system**

**Risk type: schedule risk Priority (1 low ... 5 critical): 4**

**Risk factor: Project completion will depend on tests which require hardware component under development. Hardware component** 

**delivery may be delayed**

**Probability: 60 %**

**Impact: Project completion will be delayed for each day that** 

**hardware is unavailable for use in software testing**

**Monitoring approach:**

**Scheduled milestone reviews with hardware group**

**Contingency plan:**

**Modification of testing strategy to accommodate delay using software simulation**

**Estimated resources: 6 additional person months beginning in July**

![](02_SoftwareProcess/02_SoftwareProcess/_page_57_Picture_13.jpeg)



---

# سند 3: 03_UnifiedProcess

**فایل اصلی:** `03_UnifiedProcess.pdf`

![](03_UnifiedProcess/03_UnifiedProcess/_page_0_Figure_0.jpeg)

(5% -\_\_ /

## SOFTWARE ENGINEERING COURSE

## **Unified Process**

Faezeh Gohari

# **Agenda**

- Overview of Unified Process
  - Building blocks
  - Phases, iterations and disciplines
  - UP Artifacts

![](03_UnifiedProcess/03_UnifiedProcess/_page_1_Picture_5.jpeg)

## **UP Authors**

- The first book to describe UP:
  - *The Unified Software Development Process (1999)*
  - Ivar Jacobson, Grady Booch and James Rumbaugh

![](03_UnifiedProcess/03_UnifiedProcess/_page_2_Picture_4.jpeg)

![](03_UnifiedProcess/03_UnifiedProcess/_page_2_Picture_5.jpeg)

![](03_UnifiedProcess/03_UnifiedProcess/_page_2_Picture_6.jpeg)

## **Unified Process (UP)**

- **Use Case** Driven
  - Successful system must build what users want
- **Architecture** Centric
  - Capture significant static and dynamic aspects of the system
  - Goals: understandability, reliance to future changes, and reuse
- **Iterative** and **Incremental**
- **Risk** Focused

## **UP Building Blocks**

## **Roles (who)**

- A role defines a set of related skills, competencies and responsibilities
- E.g., Project manager, System Analyst, Software Architect, Technical Writer

## **Work products (what)**

- A work product represents something resulting from a task, including all the **documents** and **models** produced
- E.g., Software Architecture Document, Software Development Plan

## **Tasks (how)**

 A task describes a unit of work assigned to a Role that provides a meaningful result

## **UP Refinements and Variations**

## **RUP**

- Rational Unified Process
- The IBM / Rational Software development process
- The best-known and extensively documented variation of UP

## OpenUP

- Open Unified Process
- The Eclipse Process Framework software development process

## AUP

- Agile Unified Process
- A lightweight variation developed by Scott W. Ambler

…

# **UP Phases, Iterations, and Disciplines**

![](03_UnifiedProcess/03_UnifiedProcess/_page_6_Figure_1.jpeg)

# **UP Life-cycle**

## Phases

- Four coarse-grained phases
- Each phase is finished before the start of the next phase

## Iterations

- Each phase is divided into iterations
- Usually 1 to 4 iterations per phase
- Iterations are also timeboxed.

## Disciplines (Workflows)

- Activities in different phases
- A discipline may continue in different phases

## **UP Phases**

- Inception
  - Understand business case, identify use cases, feasibility, cost and planning
- Elaboration
  - Detailing of use cases for this iteration, refinement of system architecture (the skeleton)
- Construction
  - Build product (put meat on the skeleton)
- Transition
  - Delivery of final product and feedback
  - Customer/User tests and interaction
  - The ongoing support

# **Disciplines**

## **Inception phase**

- By collaborating with stakeholders, basic business requirements for the software are identified.
  - Fundamental business requirements are described through a set of **preliminary use cases** that describe which major features and functions each group of users desires.
- A rough architecture for the system is proposed.
  - Architecture at this point is nothing more than a tentative outline of major subsystems and their functions and features.
- And a plan for the iterative and incremental nature of the ensuing project is developed.
  - Schedule, resources, major risks, …

# **Example Questions in Inception**

- What is the vision and business case for this project?
- Feasible?
  - Legal feasibility, Economic feasibility, Schedule feasibility, Cultural feasibility, Technical feasibility
- Buy and/or build?
  - Buy components and glue them together or from scratch?
- Estimate potential risks
- Rough estimate of cost: Is it \$10K-100K or in the millions?
- Should we proceed or stop?

## **Inception Phase Outcomes**

- A **vision** [document](#page-34-0)
  - A general vision of the core project's requirements, key features, and main constraints
- An initial **use-case model** (10% -20% complete)
- An initial project **glossary**
- An initial **[development case](#page-37-0)**
  - Specifying the process to be used (especially, the artifacts to be produced for each discipline)

# **Inception Phase Outcomes (cont.)**

- An initial risk assessment
  - **Risk list** and **Risk Management Plan**
- A project plan, showing phases and iterations scheduling
  - **Software Development Plan (SDP)**
- An initial **[business case](#page-36-0)**
  - Necessary information from a business standpoint to determine whether or not this project is worth investing in
  - Includes business context, financial forecast and success criteria (ROI, market recognition, and so on)
- One or several **prototypes**

# **Inception phase: Disciplines vs Artifacts**

 The following table shows that each artifact of the inception phase is the output of which discipline.

| Artifact                        | Discipline         |
|---------------------------------|--------------------|
| Vision                          | Requirements       |
| Use-case model                  | Requirements       |
| Glossary                        | Requirements       |
| Risk<br>list                    | Project Management |
| Risk Management Plan            | Project Management |
| Software Development Plan (SDP) | Project Management |
| Business case                   | Project Management |
| Development case                | Environment        |

## **A Simple Use Case Model**

![](03_UnifiedProcess/03_UnifiedProcess/_page_15_Picture_1.jpeg)

# **Use-Case Specification**

 A textual description detailing the sequence of events together with other related use case information in certain format

## For example:

| Use | Case | Specification |
|-----|------|---------------|
|     |      |               |

| Use Case Name:       | Withdraw Cash                                                                                                                                                                              |  |  |
|----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--|--|
| Actor(s):            | Customer (primary), Banking System (secondary)                                                                                                                                             |  |  |
| Summary Description: | Allows any bank customer to withdraw cash from their bank account.                                                                                                                         |  |  |
| Priority:            | Must Have                                                                                                                                                                                  |  |  |
| Status:              | Medium Level of details                                                                                                                                                                    |  |  |
| Pre-Condition:       | The bank customer has a card to insert into the ATM The ATM is online properly                                                                                                             |  |  |
| Post-Condition(s):   | <ul> <li>The bank customer has received their cash (and optionally a receipt)</li> <li>The bank has debited the customer's bank account and recorded details of the transaction</li> </ul> |  |  |

## **Use-Case Specification**

| Use-Case Specification |
|------------------------|
|                        |
|                        |
|                        |
|                        |
|                        |
|                        |
|                        |
|                        |
|                        |
|                        |
|                        |
|                        |
|                        |
|                        |
|                        |
|                        |
|                        |
|                        |
|                        |
|                        |
|                        |
|                        |

# **RUP Template for Use-Case Specification**

- RUP provides a standard template for recording the detailed information about use cases
- To see examples for a RUP project, refer to the link below:

https://sceweb.uhcl.edu/helm/RUP\_c [ourse\\_example/courseregistrationpro](https://sceweb.uhcl.edu/helm/RUP_course_example/courseregistrationproject/indexcourse.htm) ject/indexcourse.htm

## **Elaboration phase**

- This phase mainly focuses on modeling activities (i.e., analysis & design).
- Elaboration refines and expands the preliminary use cases.
- Expands the architectural representation to include five different views of the software:
  - **4+1 Architectural view model**
  - Use case view, logical view, process view, implementation view, deployment view
  - In some cases, elaboration creates an "executable architectural baseline".
    - A "first cut" executable system
    - Does not provide all the required features and functions
- The plan is carefully reviewed at this phase to ensure that scope, risks, and delivery dates remain reasonable.
  - Modifications to the plan are often made at this time.

## **4+1 Architectural View Model**

 Describing the architecture of software from different viewpoints:

## **1. Scenarios (use-case view)**

The description of an architecture from end-users' view

## **2. Logical view**

- The description of design model (i.e., classes, their responsibilities, relationships, ..)
- Represented by UML class diagrams

## **3. Process view**

- The description of the dynamic aspects of the system (focuses on the run time behavior)
- Explains the system processes and how they communicate
- UML diagrams to represent process view include the Data Flow Diagram (DFD), sequence diagram, communication diagram, activity diagram

![](03_UnifiedProcess/03_UnifiedProcess/_page_21_Picture_11.jpeg)

## **4+1 Architectural View Model (cont.)**

## **4. Physical view**

- Also known as implementation view
- The description of implementation model (i.e., components and subsystems)
- UML diagrams to represent physical view include package diagram and component diagram

![](03_UnifiedProcess/03_UnifiedProcess/_page_22_Picture_5.jpeg)

## **5. Deployment view**

- The description of deployment model
- Describes one or more physical network (hardware) configurations on which the software is deployed and run
  - Indicates the physical nodes (computers, CPUs) that execute the software, and their interconnections (bus, LAN, point-to-point, ...)
- Represented by UML deployment diagrams
- **Data view (optional):** A description of the persistent data storage perspective

## **Elaboration Phase Outcomes**

- **Software Requirements Specification (SRS)**
  - **Use-case model** (at least 80% complete)
    - all use-cases and actors have been identified, and most use-case descriptions have been developed.
  - **Supplementary Specifications**
    - Non-functional requirements
- A software architecture description
  - **Software Architecture Document (SAD)**
- An **executable architecture**
  - The vertical slice

![](03_UnifiedProcess/03_UnifiedProcess/_page_23_Picture_10.jpeg)

## **Elaboration Phase Outcomes (cont.)**

- A **revised risk list** and a **revised business case**
- A **revised development plan** for the overall project
- An **updated development case**

# **Elaboration phase: Disciplines vs Artifacts**

 The following table shows that each artifact of the elaboration phase is the output of which discipline.

| Artifact                                  | Discipline           |
|-------------------------------------------|----------------------|
| Software Requirements Specification (SRS) | Requirements         |
| Use-case model (updated)                  | Requirements         |
| Supplementary Specifications              | Requirements         |
| Software Architecture Document (SAD)      | Analysis<br>& Design |
| Risk list (updated)                       | Project Management   |
| Software Development Plan (updated)       | Project Management   |
| Business case (updated)                   | Project Management   |
| Development case (updated)                | Environment          |

# **Construction phase**

- Using the architectural model as input, the construction phase develops or acquires the software components that will make each use case operational for end users. To accomplish this:
  - 1. Analysis and design models that were started during the elaboration phase are completed to reflect the final version of the software increment.
  - 2. All necessary and required features and functions for the software are implemented in source code.
  - 3. As components are being implemented, unit tests are designed and executed for each.
  - 4. In addition, integration activities (component assembly and integration testing) are conducted.
  - 5. Use cases are used to derive a suite of acceptance tests that are executed prior to the initiation of the next UP phase.

# **Construction phase (cont.)**

- In addition, the software team creates the necessary **support information** that is required for the release
  - User manuals
  - Troubleshooting guides
  - Installation procedures

…

## **Construction Phase Outcomes**

- Software components
- The integrated software product

*Implementation and Test Disciplines*

- Test plan and test cases
- Support documentation
  - The user manuals, installation manuals, …
  - A description of the current release

*Deployment Discipline*

# **Transition phase**

- Software is delivered to end users for **beta testing**
- User **feedback** reports both **defects** and **necessary changes**
- At the conclusion of the transition phase, the software increment becomes a **usable software release**

## **Transition Phase Outcomes**

- Delivered software increment
- Beta test reports
- User feedbacks

*Which major disciplines?*

- *1. Deployment*
- *2. Test*
- *3. Implementation*

# **Adapt the Process**

- UP is a process framework
- Not every task identified for a UP workflow is conducted for every software project
- Many decisions are dependent on the project conditions
  - Number of iterations in a phase
  - Amount of effort (time, …) for a phase/iteration/artifact
  - The focus on documentations
- The **process engineer** should adapt the process for the target project
  - Adapting the process (actions, tasks, subtasks, and work products) to meet specific needs of the project

# **Further Reading**

- Chapter 4 of Pressman
- Search Unified Process and RUP
  - Read some wikis
  - Follow the hyperlinks:
    - [https://sceweb.uhcl.edu/helm/RationalUnifiedProcess/](https://www.ibm.com/developerworks/rational/library/content/03July/1000/12 51/1251_bestpractices_TP026B.pdf)
    - [https://www.ibm.com/support/pages/rational-unified-process-rup-plug](https://www.ibm.com/support/pages/rational-unified-process-rup-plug-ins-rational-method-composer-751)ins-rational-method-composer-751

![](03_UnifiedProcess/03_UnifiedProcess/_page_33_Picture_0.jpeg)

# **RUP Artifacts Template: Vision**

<span id="page-34-0"></span>

| Date                   | Version            | Description         | Author        |
|------------------------|--------------------|---------------------|---------------|
| <dd mmm="" yy=""></dd> | < <del>X</del> -X> | <details></details> | <name></name> |
|                        |                    |                     |               |
|                        |                    |                     |               |
|                        |                    |                     |               |

## **RUP Artifacts Template: Vision**

#### **Table of Contents**

# 1. Introduction 1.1 Purpose 1.2 Scope 1.3 Definitions, Acronyms, and Abbreviations 1.4 References 1.5 Overview 2. Positioning 2.1 Business Opportunity 2.2 Problem Statement 2.3 Product Position Statement

#### 3. Stakeholder and User Descriptions

- 3.1 Market Demographics
- 3.2 Stakeholder Summary
- 3.3 User Summary
- 3.4 User environment
- 3.5 Stakeholder Profiles
  - 3.5.1 <Stakeholder Name>
- 3.6 User Profiles
  - 3.6.1 <User Name>
- 3.7 Key Stakeholder or User Needs
- 3.8 Alternatives and Competition
  - 3.8.1 <aCompetitor>
  - 3.8.2 <anotherCompetitor>

#### 4. Product Overview

- 4.1 Product Perspective
- 4.2 Summary of Capabilities
- 4.3 Assumptions and Dependencies
- 4.4 Cost and Pricing
- 4.5 Licensing and Installation

#### 5. Product Features

- 5.1 <aFeature>
- 5.2 <anotherFeature>

#### 6. Constraints

- 7. Quality Ranges
- 8. Precedence and Priority

#### 9. Other Product Requirements

- 9.1 Applicable Standards
- 9.2 System Requirements
- 9.3 Performance Requirements
- 9.4 Environmental Requirements

#### 10. Documentation Requirements

- 10.1 User Manual
- 10.2 Online Help
- 10.3 Installation Guides, Configuration, and Read Me File
- 10.4 Labeling and Packaging

## RUP Artifacts Template: Business Case

## <Project Name> Business Case

Version <1.0>

[Note: The following template is provided for use with the Rational Unified Process. Text enclosed in square brackets and displayed in blue italics (style=InfoBlue) is included to provide guidance to the author and should be deleted before publishing the document. A paragraph entered following this style will automatically be set to normal (style=Body Text).]

#### **Revision History**

<span id="page-36-0"></span>

| Date                   | Version        | Description         | Author        |
|------------------------|----------------|---------------------|---------------|
| <dd mmm="" yy=""></dd> | < <u>x,x</u> > | <details></details> | <name></name> |
|                        |                |                     |               |
|                        |                |                     |               |
|                        |                |                     |               |

#### **Table of Contents**

- 1. Introduction
  - 1.1 Purpose
  - 1.2 Scope
  - 1.3 Definitions, Acronyms and Abbreviations
  - 1.4 References
  - 1.5 Overview
- 2. Product Description
- Business Context
- 4. Product Objectives
- 5. Financial Forecast
- 6. Constraints

## **RUP Artifacts Template: Development Case**

# <Project Name> Development Case

Version <1.0>

<span id="page-37-0"></span>[Note: The following template is provided for use with the Rational Unified Process (RUP). Text enclosed in square brackets and displayed in blue italics (style=InfoBlue) is included to provide guidance to the author and should be deleted before publishing the document. A paragraph entered following this style will automatically be set to normal (style=Body Text).]

#### **Table of Contents**

#### Introduction

- o Purpose
- o Scope
- o Definitions, Acronyms, and Abbreviations
- References
- o Overview
- Overview of the Development Case
  - o Lifecycle Model
  - o Disciplines
  - o Discipline Configuration
  - o Artifact Classification
  - o Review Procedures
  - o Sample Iteration Plans
- Disciplines
  - o Business Modeling
  - o Requirements
  - o Analysis & Design
  - o <u>Implementation</u>
  - o Testing
  - Deployment
  - o Configuration & Change Management
  - o Project Management
  - o <u>Environment</u>
- Roles



---

# سند 4: 04_AgileProcesses

**فایل اصلی:** `04_AgileProcesses.pdf`

# **Agile Development**

#### **Agile Processes: Chapter 5**

*Slide Set to accompany*

*Software Engineering: A Practitioner's Approach, 8/e*

**by Roger S. Pressman and Bruce R. Maxim**

**Slides copyright © 1996, 2001, 2005, 2009, 2014 by Roger S. Pressman**

#### *For non-profit educational use only*

May be reproduced ONLY for student use at the university level when used in conjunction with *Software Engineering: A Practitioner's Approach, 8/e.* Any other reproduction or use is prohibited without the express written permission of the author.

All copyright information MUST appear if these slides are posted on a website for student use.

## Agenda

- Overview of Agile Development
  - Agile Principles
- Agile Processes
  - XP
  - Scrum
  - Other Agile Methodologies

![](04_AgileProcesses/04_AgileProcesses/_page_1_Picture_7.jpeg)

# *Overview*

#### The Manifesto for Agile Software Development

**"We are uncovering better ways of developing software by doing it and helping others do it. Through this work we have come to value:** 

- •*Individuals and interactions* **over processes and tools**
- •*Working software* **over comprehensive documentation**
- •*Customer collaboration* **over contract negotiation**
- •*Responding to change* **over following a plan That is, while there is value in the items on the**

**right, we value the items on the left more."**

*Kent Beck et al*

# What is "Agility"?

- Effective (rapid and adaptive) response to change
- Effective communication among all stakeholders
- Rapid delivery of operational software
- Drawing the customer onto the team
- Organizing a team so that it is in control of the work performed
  - Flexible planning in an uncertain world

#### *Yielding …*

Rapid, incremental delivery of software

# Agility and the Cost of Change

![](04_AgileProcesses/04_AgileProcesses/_page_5_Figure_1.jpeg)

# The Applicability of Agile

- Agile development can provide important benefits, but it is not applicable to all projects, all products, all people, and all situations
- In the modern economy, we need agility when:
  - Market conditions change rapidly, end-user needs evolve, and new competitive threats emerge without warning
  - Requirements cannot be fully identified before the project begins (we must be agile enough to respond to a fluid business environment)
- Agile Processes ≈ Light or Lean Processes

#### Considerations to Accomplish Agility

- Design the process in a way that allows the project team to adapt tasks.
- Conduct flexible planning that understands the fluidity of an agile development approach.
- Eliminate all but the most essential work products and keep them lean.
- Emphasize an incremental delivery strategy that gets working software to the customer as rapidly as feasible.
  - Short-time increments
  - Adaptation keeps pace with change

# An Agile Process

- Is driven by customer descriptions of what is required (scenarios)
- Recognizes that plans are short-lived
- Develops software iteratively with a heavy emphasis on construction activities
- Delivers multiple 'software increments'
- Adapts as changes occur

# Agility Principles - I

- 1. Our highest priority is to satisfy the customer through early and continuous delivery of valuable software.
- 2. Welcome changing requirements, even late in development. Agile processes harness change for the customer's competitive advantage.
- 3. Deliver working software frequently, from a couple of weeks to a couple of months, with a preference to the shorter timescale.
- 4. Business people and developers must work together daily throughout the project.
- 5. Build projects around motivated individuals. Give them the environment and support their need, and trust them to get the job done.
- 6. The most efficient and effective method of conveying information to and within a development team is face–to–face conversation.

# Agility Principles - II

- 7. Working software is the primary measure of progress.
- 8. Agile processes promote sustainable development. The sponsors, developers, and users should be able to maintain a constant pace indefinitely.
- 9. Continuous attention to technical excellence and good design enhances agility.
- 10. Simplicity the art of maximizing the amount of work not done – is essential.
- 11. The best architectures, requirements, and designs emerge from self–organizing teams.
- 12. At regular intervals, the team reflects on how to become more effective, then tunes and adjusts its behavior accordingly.

# *Extreme Programming (XP)*

# Extreme Programming (XP)

- The most widely used agile process
- Originally proposed by Kent Beck
- XP uses an objectoriented approach

![](04_AgileProcesses/04_AgileProcesses/_page_12_Picture_4.jpeg)

# XP Planning

- Begins with the creation of "user stories"
- Each story is written by the customer and is placed on an index card (called story card)
- Customer assigns a value (i.e., a priority) to the story
- Agile team assesses each story and assigns a cost
  - Measured in development weeks
  - Typical story points: 1, 2, 3, or "too big"
  - If the story requires more than three weeks, the customer is asked to split the story into smaller stories
- Stories are grouped for a deliverable increment
- A commitment is made on delivery date

# Sample Story Cards

| As a customer, I want to be able to sear<br>for flights between two cities to see wh<br>ones have the best price and route. |                                                                                                           |                                             |                                                                                                                                                                                                                           |                          |
|-----------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|---------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------|
|                                                                                                                             | NO: 16                                                                                                    | Project Name E-Commerce                     | Estimation: 4 H                                                                                                                                                                                                           | lours                    |
| Estimate: 1.0 points                                                                                                        | Story Name: User Registration                                                                             |                                             |                                                                                                                                                                                                                           | Date: 16/08/2007 1:30 PM |
| Priority: 2 - High                                                                                                          | STORY:                                                                                                    |                                             | Acceptance Test:                                                                                                                                                                                                          |                          |
| Example Story Card                                                                                                          | User needs to register with unique username and password before purchasing anything from the online store |                                             | <ol> <li>User Id must be unique</li> <li>Try to register with duplicate user id and Password</li> <li>Try to register user name only</li> <li>Try to register with password only</li> <li>Forget Password Link</li> </ol> |                          |
|                                                                                                                             | Note: User Can View or Visit store as a Visitor but needs to register before purchasing anything          |                                             | Risk: Low                                                                                                                                                                                                                 |                          |
|                                                                                                                             | Points to be Co                                                                                           | onsider:<br>re isn't any non-functional req | pairement at this s                                                                                                                                                                                                       | rtage                    |

![](04_AgileProcesses/04_AgileProcesses/_page_15_Picture_0.jpeg)

# XP Planning (cont.)

- After each increment, "project velocity" is computed to help define the delivery date of the next increment
  - Project velocity is the number of customer stories implemented during the iteration
- Note: new stories can be written at any time
  - As development work proceeds, the customer can add stories, change the value of an existing story, split stories, or eliminate them
  - The XP team then reconsiders all remaining releases and modifies its plans accordingly

# XP Design

- Keep It Simple (KISS principle)
  - The design of extra functionality is discouraged
- Encourages the use of CRC cards (see Chapter 8)
  - Class-Responsibility-Collaborator
- For difficult design problems, suggests the creation of "spike solutions"—a design prototype
- Encourages "refactoring"—an iterative refinement of the internal program design
  - It is a construction technique that is also a design technique
  - Small changes that "can radically improve the design"
- In XP, design occurs both before and after coding commences

# A Sample CRC Card

![](04_AgileProcesses/04_AgileProcesses/_page_17_Picture_1.jpeg)

| Class Name       |               |  |
|------------------|---------------|--|
| Responsibilities | Collaborators |  |

# XP Coding

- Recommends the construction of a unit test for a story *before* coding commences
- Encourages "pair programming"
  - Real-time **code review**
- Emphasizes "continuous integration"

![](04_AgileProcesses/04_AgileProcesses/_page_18_Picture_5.jpeg)

# XP Testing

![](04_AgileProcesses/04_AgileProcesses/_page_19_Picture_1.jpeg)

- All unit tests are executed daily
  - Must be **automated**
- Daily testing provides can raise warning flags early
  - "Fixing small problems every few hours takes less time than fixing huge problems just before the deadline"
- **Regression testing**
- "Acceptance tests" are executed to assess customer visible functionality
  - Also called customer tests
  - Derived from user stories

## XP Practices

![](04_AgileProcesses/04_AgileProcesses/_page_20_Figure_1.jpeg)

## XP Practices: Whole Team

- All contributors to an XP project are **one team**
- Must include a business representative (the 'Customer')
  - Provides requirements
  - Sets priorities
  - Guides project
- Team members: programmers, testers, analysts,

manager, …

![](04_AgileProcesses/04_AgileProcesses/_page_21_Picture_8.jpeg)

# XP Practices: Planning Game

- The planning process within XP:
  - **The Planning Game**
- The game is a meeting that occurs once per iteration
  - Typically once a week
- The planning process is divided into two parts:
  - **Release Planning**
    - What requirements are included in near-term releases?
    - When they should be delivered?
  - **Iteration Planning**
    - Plans the activities and tasks of the developers

## XP Practices: Customer Tests

- The Customer defines **automated acceptance tests**
  - for each feature
- Team builds these tests and uses them
  - to prove (to themselves and to the customer) that a feature is implemented correctly
- The best XP teams treat customer tests the same way as programmer tests:
  - Once the test runs, the team ensures that it **keeps running** correctly thereafter
  - System always improves, always notching forward, never backsliding

## XP Practices: Small Releases

- Team releases **running**, **tested** software
  - In every iteration
- Releases are **small** and **functional**
- The customer can evaluate and provide **feedback**
- The software is **visible**
  - It is given to the customer at the end of every iteration

# XP Practices: Simple Design

- Build software to a **simple** but always **adequate** design
- Start simple and **Keep it that way**
  - Through programmer testing and design improvement
- Good design is essential in XP
- Not a one-time thing
- Teams design and revise design through **refactoring**
  - Throughout the course of the project

# XP Practices: Pair Programming

- Software is built by two programmers
  - Sitting side by side, at the same machine
- A better mechanism for **problem solving** 
  - Two heads are often better than one
- All production code is reviewed by at least one other programmer
  - **Real-time quality assurance**

*Researches show that pairing produces better code in the same time as programmers working singly*

![](04_AgileProcesses/04_AgileProcesses/_page_26_Picture_8.jpeg)

#### XP Practices: Test-Driven Development

- Writing tests **first**
- Short cycles of adding a test, **and then** making it work
- Nearly 100 percent code coverage
  - Code coverage: The degree to which the source code is tested by the test suite
- The unit tests are all collected together
- Each time a pair releases any code to the **repository** (pairs typically release twice a day or more):
  - Every test must run correctly

## XP Practices: Refactoring

- Continuous design improvement process
  - Removal of duplication
  - Increase cohesion
  - Reduce coupling
- Bad Smells and Refactoring techniques
- Supported by comprehensive testing
  - to be sure that as the design improves, nothing is broken
  - customer tests and programmer tests are a critical enabling factor
  - XP practices support each other

![](04_AgileProcesses/04_AgileProcesses/_page_28_Picture_10.jpeg)

#### XP Practices: Continuous Integration

- Keep the system **fully integrated at all times**
- **Daily**, or multiple times a day builds
- Integration is not a phase nor a postponable activity
- Avoid "**integration hell**"
  - where everything broke and no one knew why
- It helps to uncover errors **early**

# XP Practices: Collective Code Ownership

- **Any pair** of programmers can improve **any code** at **any time**
- No **'secure workspaces'**
- All code gets the benefit of many people's attention
  - increases code quality and reduces defects
- **Avoid duplication**
- Pair with the expert when working on unfamiliar code

# XP Practices: Coding Standard

- Follow a common coding standard
- All code in the system must look as if it was written by a single individual
- Code must look familiar, to support collective code ownership
- Coding Conventions
  - Comment conventions
  - Indent style conventions
  - Naming conventions
  - …

## XP Practices: Metaphor

- XP Teams develop a common vision of the system, called "metaphor"
- A simple description of how the program works
- XP teams use a common system of names (i.e., shared vocabulary)
- Ensure everyone understands how the system works
  - where to look for a functionality
  - or where to add a functionality

## XP Practices: Sustainable Pace

- Team will produce high quality product when not overly exerted
- Avoid overtime, maintain **40 hour weeks**
- **'Death march' projects are unproductive**
  - and do not produce quality software
- Work at a pace that can be **sustained indefinitely**

## XP Values

- Communication
- Simplicity
- Feedback
- Courage
- Respect

![](04_AgileProcesses/04_AgileProcesses/_page_34_Picture_6.jpeg)

## XP Values: Communication

- 'We will work together on everything from requirements to code'
- **Poor communication** in software teams:
  - one of the root causes of failure of a project
- Stress on good communication between **all** stakeholders
  - customers, team members, project managers
- Customer representative always on site

# Example: Daily Stand Up Meeting

- Purpose: communication among the entire team
- Every morning
- To communicate problems and solutions

![](04_AgileProcesses/04_AgileProcesses/_page_36_Picture_4.jpeg)

- Everyone stands up in a circle to avoid long discussions
- One short meeting
  - Every one is required to attend
  - More efficient than many meetings with a few developers each

![](04_AgileProcesses/04_AgileProcesses/_page_36_Picture_9.jpeg)

# XP Values: Simplicity

- 'Do the **Simplest** Thing That Could Possibly Work'
  - Implement a new capability in the simplest possible way
  - Refactor the system to be the simplest possible code
- 'You Aren't Going to Need It'
  - Never implement a feature you don't need now

## XP Values: Feedback

- Always a running system that delivers information about itself in a reliable way
- The system and the code provides feedback on the state of development
- Catalyst for change and an indicator of progress

## XP Values: Courage

- We will tell the truth about progress and estimates
- We don't fear anything because **no one ever works alone**
- We will adapt to changes when ever they happen

## *SCRUM*

## Scrum

- Originally proposed by Schwaber and Beedle
- An iterative and incremental agile methodology
  - For managing product development
- It is agile, so it appreciates:
  - Accept change, Good Communication, Customer Collaboration, …
- Scrum defines specific roles, events, and artifacts

*The name is derived from rugby (an activity that occurs during a rugby game) to stress the importance of working as a team in complex product development*

# Scrum Framework at a glance

![](04_AgileProcesses/04_AgileProcesses/_page_42_Figure_1.jpeg)

## Scrum Roles

#### **Product owner**

- Represents the stakeholders
- and is the voice of customer

#### **Scrum master**

- Ensures that the scrum process is used as intended
- Coaching the team

#### **Development team**

 Responsible for delivering increments

![](04_AgileProcesses/04_AgileProcesses/_page_43_Figure_9.jpeg)

# Scrum Sprints

- A **sprint** (or iteration)
  - The basic unit of development in scrum
- The sprint is a time-boxed effort (typically two weeks)
- Scrum emphasizes working product at the end of the sprint
  - That is really *done*.
  - E.g. the software has been **integrated**, fully **tested**, **end-user documented**, and is **potentially shippable**
- The number of sprints depends on product complexity and size

![](04_AgileProcesses/04_AgileProcesses/_page_44_Picture_9.jpeg)

## Scrum Events

#### **1. Sprint planning**

At the beginning of a sprint

#### **2. Daily scrum meeting**

- All members of the development team come prepared
- Starts precisely **on time** (even if some members are missing)
- Should happen at the same time and place every day
- Is limited to **15 minutes**
- At the end of a sprint:
  - **3. Sprint review**
  - **4. Sprint retrospective**

# Daily Scrum Meeting

- Every day
- Very short (typically 15-minute)
- Three key questions are asked and answered by all team members:
- 1. What did you do since the last team meeting?
- 2. What obstacles are you encountering?
- 3. What do you plan to accomplish by the next team meeting?
- Scrum master leads the meeting and assesses the responses from each person

## Daily Scrum: Benefits

- Helps the team to uncover potential problems as early as possible
- Lead to "knowledge socialization"
  - promote a self-organizing team structure

![](04_AgileProcesses/04_AgileProcesses/_page_47_Picture_4.jpeg)

## At the End of a Sprint:

#### **Sprint review**

- Reviews the work that was completed
- Presents the completed work to the stakeholders (**demo**)
  - Incomplete work cannot be demonstrated
- The recommended duration: 2 hours for a two-week sprint

#### **Sprint retrospective**

- What went well during the sprint?
- What could be improved in the next sprint?
- The recommended duration: 1.5 hours for a two-week sprint
- This event is facilitated by the **scrum master**

## Scrum Artifacts

#### **Product backlog**

- An **ordered** list of product requirements
- Includes: Features, bug fixes, non-functional requirements, etc.
- The **product owner** orders the product backlog items
- **Sprint backlog** (*the output of sprint planning*)
  - The works the development team must address during a sprint
  - By selecting product backlog items **from the top** of the product backlog
  - Broken down into tasks by the development team
  - Often a **task board** is used: the state of the tasks of the current sprint
    - Like: "*to do*", "*in progress*", and "*done*"

![](04_AgileProcesses/04_AgileProcesses/_page_50_Figure_0.jpeg)

## Scrum Board

![](04_AgileProcesses/04_AgileProcesses/_page_50_Picture_2.jpeg)

# Scrum Artifacts (cont.)

#### **Product increment**

potentially shippable increment (PSI)

#### **Sprint burn-down chart**

- A **public** displayed chart
- Shows remaining work in the sprint backlog
- Updated every day:
- gives a simple view of the sprint progress

![](04_AgileProcesses/04_AgileProcesses/_page_51_Figure_8.jpeg)

## Scrum vs XP?

- Scrum doesn't prescribe any engineering practices; XP does.
  - Scrum is an agile **management methodology**
  - XP is an agile **engineering methodology**
  - As such they are entirely **complementary**
- Minor differences:
  - XP iterations: 1-2 weeks, Scrum sprints: 1-4 weeks (usually longer)
  - Scrum doesn't allow changes to the sprint backlog during the sprint

## Scrum/XP Hybrid

- Many teams use both Scrum and XP
  - Scrum template for project management
  - XP practices for technical tasks

(XP and Scrum complement each other)

![](04_AgileProcesses/04_AgileProcesses/_page_53_Figure_5.jpeg)

## *Other Agile Methodologies*

# Other Agile Methodologies

- Agile Unified Process (AUP)
- Dynamic Systems Development Method (DSDM)
- Agile Modeling (AM)
- Feature Driven Development (FDD)
- Adaptive Software Development (ASD)
- Crystal
- ….

# Agile Unified Process

- AUP adopts a "serial in the large" and "iterative in the small" philosophy
- Serial in the Large
  - Four phases: Inception, Elaboration, Construction, Transition
- Iterative in the small
  - Disciplines are performed in an iterative manner
  - Seven disciplines:
    - Modeling, Implementation, Testing, Deployment, Configuration Management, Project Management, Environment

# Agile Unified Process

![](04_AgileProcesses/04_AgileProcesses/_page_57_Figure_1.jpeg)

# Further Reading

| PART ONE  | THE SOFTWARE PROCESS 29                  |
|-----------|------------------------------------------|
| CHAPTER 3 | Software Process Structure 30            |
| CHAPTER 4 | Process Models 40                        |
| CHAPTER 5 | Agile Development 66                     |
| CHAPTER 6 | Human Aspects of Software Engineering 87 |

- Search about agile processes
  - and read some tutorials/wikis/ppts/…
  - About:
    - XP
    - SCRUM
    - …

## *The End*



---

# سند 5: 05_RequirementsEngineering

**فایل اصلی:** `05_RequirementsEngineering.pdf`

### **Requirements Engineering**

#### **Modeling: Chapters 8-11**

*Slide Set to accompany*

*Software Engineering: A Practitioner's Approach, 8/e*

**by Roger S. Pressman and Bruce R. Maxim**

**Slides copyright © 1996, 2001, 2005, 2009, 2014 by Roger S. Pressman**

#### *For non-profit educational use only*

May be reproduced ONLY for student use at the university level when used in conjunction with *Software Engineering: A Practitioner's Approach, 8/e.* Any other reproduction or use is prohibited without the express written permission of the author.

All copyright information MUST appear if these slides are posted on a website for student use.

### Agenda

- Understanding Requirements
- Requirements Modeling
  - Scenario-Based Methods
  - Class-Based Methods
  - Behavioral Methods
  - Requirements Modeling for Web and Mobile Apps

### *Understanding Requirements*

# Requirements Engineering-I

- Inception—ask a set of questions that establish …
  - basic understanding of the problem
  - the people who want a solution
  - the nature of the solution that is desired, and
  - effective communication and collaboration between the customer and the developer
- Elicitation—elicit requirements from all stakeholders
- Elaboration—expand and refine the information obtained during inception and elicitation
  - **Requirements modeling**: create an analysis model that identifies data, function and behavioral requirements
- Negotiation—agree on a deliverable system that is realistic for developers and customers

# Requirements Engineering-II

- Specification—can be any one (or more) of the following:
  - A written document
  - A set of models
  - A formal mathematical
  - A collection of user scenarios (use-cases)
  - A prototype
- Validation—a review mechanism that looks for
  - errors in content or interpretation
  - areas where clarification may be required
  - missing information
  - inconsistencies (a major problem when large products or systems are engineered)
  - conflicting or unrealistic (unachievable) requirements.
- Requirements management— control and track changes to requirements at any time
  - Many of these tasks are supported by the software configuration management (SCM)

# A Sample Template for Requirements Specification

INFO

#### Software Requirements Specification Template

A software requirements specification (SRS) is a work product that is created when a detailed description of all aspects of the software to be built must be specified before the project is to commence. It is important to note that a formal SRS is not always written. In fact, there are many instances in which effort expended on an SRS might be better spent in other software engineering activities. However, when software is to be developed by a third party, when a lack of specification would create severe business issues, or when a system is extremely complex or business critical, an SRS may be justified.

Karl Wiegers [Wie03] of Process Impact Inc. has developed a worthwhile template (available at www.processimpact.com/process\_assets/srs\_template.doc) that can serve as a guideline for those who must create a complete SRS. A topic outline follows:

#### **Table of Contents**

#### **Revision History**

#### 1. Introduction

- 1.1 Purpose
- 1.2 Document Conventions
- 1.3 Intended Audience and Reading Suggestions
- 1.4 Project Scope
- 1.5 References

#### 2. Overall Description

- 2.1 Product Perspective
- 2.2 Product Features
- 2.3 User Classes and Characteristics
- 2.4 Operating Environment
- 2.5 Design and Implementation Constraints
- 2.6 User Documentation
- 2.7 Assumptions and Dependencies

#### 3. System Features

- 3.1 System Feature 1
- 3.2 System Feature 2 (and so on)

#### 4. External Interface Requirements

- 4.1 User Interfaces
- 4.2 Hardware Interfaces
- 4.3 Software Interfaces
- 4.4 Communications Interfaces

#### 5. Other Nonfunctional Requirements

- 5.1 Performance Requirements
- 5.2 Safety Requirements
- 5.3 Security Requirements
- 5.4 Software Quality Attributes

#### 6. Other Requirements

**Appendix A: Glossary** 

**Appendix B: Analysis Models** 

Appendix C: Issues List

A detailed description of each SRS topic can be obtained by downloading the SRS template at the URL noted in this sidebar.

# A Sample Checklist for Requirements Validation

#### Info

#### Requirements Validation Checklist

It is often useful to examine each requirement against a set of checklist questions. Here is a small subset of those that might be asked:

- Are requirements stated clearly? Can they be misinterpreted?
- Is the source (e.g., a person, a regulation, a document) of the requirement identified? Has the final statement of the requirement been examined by or against the original source?
- Is the requirement bounded in quantitative terms?
- What other requirements relate to this requirement?
   Are they clearly noted via a cross-reference matrix or other mechanism?

- Does the requirement violate any system domain constraints?
- Is the requirement testable? If so, can we specify tests (sometimes called validation criteria) to exercise the requirement?
- Is the requirement traceable to any system model that has been created?
- Is the requirement traceable to overall system/ product objectives?
- Is the specification structured in a way that leads to easy understanding, easy reference, and easy translation into more technical work products?
- Has an index for the specification been created?
- Have requirements associated with performance, behavior, and operational characteristics been clearly stated? What requirements appear to be implicit?

#### Inception

- Identify stakeholders
  - "who else do you think I should talk to?"
- Recognize multiple points of view
- Work toward collaboration
- The first questions
  - Who is behind the request for this work?
  - Who will use the solution?
  - What will be the economic benefit of a successful solution?
  - Is there another source for the solution that you need?
    - possible alternatives to custom software development

#### Eliciting Requirements

- meetings are conducted and attended by both software engineers and customers
- rules for preparation and participation are established
- an agenda is suggested
- a "facilitator" (can be a customer, a developer, or an outsider) controls the meeting
- the goal is
  - to explore the problem
  - propose elements of the solution
  - specify a preliminary set of solution requirements

## Quality Function Deployment

- QFD is a quality management technique that translates unspoken customer needs into system requirements
- QFD emphasizes an understanding of what is **valuable** to the customer and then deploys these values throughout the engineering process
- 1. Normal requirements—objectives and goals that are **stated** for a product to satisfy customers
- 2. Expected requirements—**implicit** requirements that their absence will be a cause for significant dissatisfaction
- 3. Exciting requirements—**beyond** customer expectations and prove to be very satisfying when present
- Customer voice table

## Usage Scenarios (Use-Cases)

- As requirements are gathered, an overall vision of system functions and features begin to materialize
- However, it is difficult to move into more technical SE activities until you understand how these functions and features will be used by different classes of users
- To do this, developers and users can create a set of scenarios that identify a thread of usage for the system
- The scenarios, often called use cases
  - provide a description of how the system will be used
- Each scenario is described from the point-of-view of an "actor"—a person or device that interacts with the software in some way

#### **Use-Case Diagram**

![](05_RequirementsEngineering/05_RequirementsEngineering/_page_11_Picture_1.jpeg)

### Non-Functional Requirements

- Non-Functional Requirement (NFR) quality attribute, performance attribute, security attribute, or general system constraint.
- A two phase process is used to determine which NFR's are compatible:
  - The first phase is to create a matrix using NFRs as column labels and SE guidelines as row labels
    - classifying each NFR and guideline pair as complementary, overlapping, conflicting, or independent
  - The second phase is for the team to prioritize and create a homogeneous set of NFRs using a set of rules to decide which to implement

### Agile Requirements Elicitation

- Within the context of an agile process, requirements are elicited by asking all stakeholders to create user stories
- Although the agile approach to requirements elicitation is attractive for many software teams, critics argue that:
  - overall business goals and nonfunctional requirements are often lacking
- In some cases, rework is required to accommodate performance and security issues
- In addition, user stories may not provide a sufficient basis for system evolution over time

# Activity Diagram of Requirements Elicitation

![](05_RequirementsEngineering/05_RequirementsEngineering/_page_14_Figure_1.jpeg)

### Building the Analysis Model

- Intent: provides a description of the required **informational**, **functional**, and **behavioral** domains of a system
- a snapshot of requirements at any given time
- changes dynamically as you learn more about the system
- As the analysis model evolves, certain elements will become relatively stable
  - providing a solid foundation for the design tasks that follow

### Elements of the Analysis Model

- Scenario-based elements
  - Use-case—descriptions of the interaction between an "actor" and the system
  - Activity Diagram—processing narratives for software functions
- Class-based elements
  - Class diagram
- Behavioral elements
  - State diagram
  - Sequence diagram

#### Scenario-Based Elements

- The system is described from the user's point of view using a scenario
- Often the first part of the analysis model
- Serve as input for the creation of other modeling elements
- Use-case diagram
- Use-case description
- Activity diagram

#### Class-Based Elements

- Each usage scenario implies a set of objects that are manipulated during the scenario
- UML class diagram depicts the structures of classes

#### **From the** *SafeHome* **system …**

#### Sensor name/id type location area characteristics identify() enable() disable() reconfigure ()

#### Behavioral Elements

- The behavior of a system can have a profound effect on the design that is chosen and the implementation approach
- The state diagram is **one method** for representing the behavior of a system
  - Depicting its states and the events that cause the system to change state
- **State diagram**
- Events (or transitions) represented by:
- Each state may define the following actions:
  - *entry/*, exit/, *do*/, and *include*/

## State Diagram Example

Consider a software to be built for a sophisticated print shop. The overall intent of the software is to collect the customer's requirements at the front counter, cost a print job, and then pass the job on to an automated production facility

![](05_RequirementsEngineering/05_RequirementsEngineering/_page_20_Figure_2.jpeg)

### Negotiating Requirements

- Asking stakeholders to balance functionality, performance, and other requirements against cost and time-to-market
- The best negotiations strive for a "**win-win**" result
- Stakeholders win by getting a product that satisfies the majority of their needs and you (as a member of the software team) win by working to realistic and achievable budgets and deadlines

#### Negotiation Activities

- Identify the key stakeholders
  - These are the people who will be involved in the negotiation
- Determine each of the stakeholders "win conditions"
  - Win conditions are not always obvious
- Negotiate
  - Work toward a set of requirements that lead to "winwin"

### Validating Requirements - I

- A review of the requirements model addresses the following questions:
- Is each requirement consistent with the overall objective for the system/product?
- Have all requirements been specified at the proper level of abstraction? That is, do some requirements provide a level of technical detail that is inappropriate at this stage?
- Is the requirement really necessary or does it represent an add-on feature that may not be essential to the objective of the system?
- Is each requirement bounded and unambiguous?

### Validating Requirements - II

- Does each requirement have attribution? That is, is a source (generally, a specific individual) noted for each requirement?
- Do any requirements conflict with other requirements?
- Is each requirement achievable in the technical environment that will house the system or product?
- Is each requirement testable, once implemented?
- Does the requirements model properly reflect the information, function and behavior of the system to be built?
- ….

### Requirements Monitoring

- Extremely needed in **incremental** development
- Incremental development implies the need for incremental validation
- Requirements monitoring supports continuous validation
  - *Run-time verification*  determines whether software matches its specification.
  - *Run-time validation*  assesses whether evolving software meets user goals.
  - *Distributed debugging*  uncovers the root cause of errors.
  - *Business activity monitoring*  evaluates whether a system satisfies business goals.
  - *Evolution and co-design*  provides information to stakeholders as the system evolves.

#### *Requirements Modeling*

#### Requirements Analysis

- Requirements analysis allows the software engineer (called an *analyst* or *modeler* in this role) to:
  - elaborate on basic requirements established during earlier requirement engineering tasks
  - build models that depict
    - user scenarios
    - functional activities
    - problem classes and their relationships
    - system and class behavior
    - and the flow of data as it is transformed

#### Elements of Requirements Analysis

![](05_RequirementsEngineering/05_RequirementsEngineering/_page_28_Picture_1.jpeg)

### Requirements Modeling

- Scenario-based models
  - Depict the system from the user's point of view
- Class-oriented models
  - Define classes (attributes and operations) and their relationships
- Behavioral models
  - Show how the software behaves as a consequence of external "events"
- Data models
  - Depict the information domain for the problem
- Flow-oriented models
  - Show how data are transformed inside the system

#### A Bridge

![](05_RequirementsEngineering/05_RequirementsEngineering/_page_30_Picture_1.jpeg)

#### Domain Analysis

 Some analysis problems often reoccur across many applications within a specific business domain

Software domain analysis is the identification, analysis, and specification of **common requirements** from a **specific application domain**, typically for **reuse** on multiple projects within that application domain . . . [Object-oriented domain analysis is] the identification, analysis, and specification of common, reusable capabilities within a specific application domain, in terms of common objects, classes, subassemblies, and frameworks . . .

#### Domain Analysis

- Application domain can range from avionics to banking, from multimedia video games to software embedded within medical devices
- The goal of domain analysis:
  - find and create those analysis classes that are broadly applicable so that they may be reused

#### Steps:

- Define the domain to be investigated.
- Collect a representative sample of applications in the domain.
- Analyze each application in the sample.
- Develop an analysis model for the objects.

# *Requirements Modeling: Scenario-Based Methods*

#### Scenario-Based Modeling

"[Use-cases] are simply an aid to defining what exists outside the system (actors) and what should be performed by the system (use-cases)."

Ivar Jacobson

- Typical elements for scenario-based modeling:
  - Use-case diagram
  - Use-case description
  - Activity diagram

#### Developing a Use-Case

- When looking for use cases, ask the following questions:
  - What are the main tasks of the actor?
  - What information does the actor need from the system?
  - What information does the actor provide to the system?
  - Does the system need to inform the actor of any changes or events that have occurred?
  - Does the actor need to inform the system of any changes or events that have occurred?

### Use-Case Diagram

![](05_RequirementsEngineering/05_RequirementsEngineering/_page_36_Picture_1.jpeg)

#### Activity Diagram

*Supplements the use case by providing a graphical representation of the flow of interaction within a specific scenario*

![](05_RequirementsEngineering/05_RequirementsEngineering/_page_37_Figure_2.jpeg)

**Activity diagram for Access camera surveillance via the Internet display camera view function**

#### Swimlane Diagrams

*A variation of the activity diagram that allows the modeler to represent the flow of activities described by the use-case and at the same time indicate which actor (if there are multiple actors involved in a specific use-case) or analysis class has responsibility for the action described by an activity rectangle*

![](05_RequirementsEngineering/05_RequirementsEngineering/_page_38_Figure_2.jpeg)

# *Requirements Modeling: Class-Based Methods*

#### Class-Based Modeling

- Class-based modeling represents:
  - objects that the system will manipulate
  - operations (also called methods or services) that will be applied to the objects to effect the manipulation
  - relationships (some hierarchical) between the objects
  - collaborations that occur between the classes that are defined.
- The elements of a class-based model include classes and objects, attributes, operations, CRC models, collaboration diagrams and packages.

### Identifying Analysis Classes

- Examining the usage scenarios developed as part of the requirements model and perform a "grammatical parse" [Abb83]
  - Classes are determined by underlining each **noun or noun phrase** and entering it into a simple table.
  - Synonyms should be noted.
  - If the class (noun) is required to implement a solution, then it is part of the solution space
  - Example:

 But what should we look for once all of the nouns have been identified?

#### Manifestations of Analysis Classes

- *Analysis classes* manifest themselves in one of the following ways:
  - *External entities* (e.g., other systems, devices, people) that produce or consume information
  - *Things* (e.g, reports, displays, letters, signals) that are part of the information domain for the problem
  - *Occurrences or events* (e.g., a property transfer or the completion of a series of robot movements) that occur within the context of system operation
  - *Roles* (e.g., manager, engineer, salesperson) played by people who interact with the system
  - *Organizational units* (e.g., division, group, team) that are relevant to an application
  - *Places* (e.g., manufacturing floor or loading dock) that establish the context of the problem and the overall function
  - *Structures* (e.g., sensors, four-wheeled vehicles, or computers) that define a class of objects or related classes of objects

#### Defining Attributes

- Study each use case and select those "things" that reasonably "belong" to the class
- Ask this question for each class:
  - *What data items fully define this class in the context of the problem at hand?*

#### Example:

- Consider the **System** class defined for SafeHome
- A homeowner can configure the system to reflect sensor information, alarm information, activation or deactivation information, identification information, …

#### Defining Operations

- Do a grammatical parse of a processing narrative and look at the **verbs**
- For example, from the SafeHome processing narrative:
  - "sensor is assigned a number and type"
  - "a master password is programmed for arming and disarming the system."
  - These phrases indicate a number of things:
    - assign() operation is relevant for the Sensor class.
    - program() operation will be applied to the System class.
    - arm() and disarm() are operations that apply to System class

#### CRC Models

- *Class-responsibility-collaborator (CRC) modeling* [Wir90] provides a **simple** means for identifying and organizing the classes
- Ambler [Amb95] describes CRC modeling in the following way:
  - A CRC model is really a collection of standard index cards that represent classes. The cards are divided into three sections. Along the top of the card you write the name of the class. In the body of the card you list the class responsibilities on the left and the collaborators on the right.

#### **CRC Modeling**

![](05_RequirementsEngineering/05_RequirementsEngineering/_page_46_Picture_1.jpeg)

#### Responsibilities

- Each responsibility should be stated as generally as possible
  - general responsibilities (both attributes and operations) should reside high in the class hierarchy
- Information and the behavior related to it should reside within the same class
  - encapsulation
- Information about one thing should be localized with a single class, not distributed across multiple classes.
- Responsibilities should be shared among related classes, when appropriate.
  - Consider a video game with four classes: **Player**, **PlayerBody**, **PlayerArms**, **PlayerLegs**, **PlayerHead**.
  - Each class has its own attributes (e.g., position, orientation, …) and must be updated and displayed as the user manipulates
  - The responsibilities update and display must therefore be shared

#### Collaborations

- Collaborations are identified by determining whether a class can fulfill each responsibility itself
- If it cannot, then it needs to interact with another class.
- Collaborations identify relationships between classes
- Three different generic relationships between classes [WIR90]:
  - the *is-part-of* relationship (for example, **PlayerHead** and **Player**)
  - the *has-knowledge-of* relationship
    - one class must acquire information from another class
  - the *depends-upon* relationship
    - Not achieved *by has-knowledge-of* or *is-part-of*.
    - For example, **PlayerHead** must always be connected to **PlayerBody**
    - Yet each object could exist without direct knowledge of the other
    - An attribute of the **PlayerHead** object called center-position is determined from the center position of **PlayerBody**
    - This information is obtained via a third object, **Player**, that acquires it from **PlayerBody**. Hence, **PlayerHead** depends-upon **PlayerBody**

### Composite Aggregate Class

![](05_RequirementsEngineering/05_RequirementsEngineering/_page_49_Picture_1.jpeg)

#### UML Class Diagram

- Remind:
  - Standard Notations
  - Associations
    - Multiplicity
  - Dependencies
  - Composition and Aggregation
  - Specialization/Generalization
  - …

### Analysis Packages

- An important part of analysis modeling is **categorization**
- Various elements of the analysis model (e.g., use-cases, analysis classes) are categorized as a grouping
  - Called an *analysis package*
- Given a representative name
- The plus sign preceding the analysis class name in each package indicates that
  - the classes have public visibility and accessible from other packages
- A minus sign indicates that an element is hidden from all other packages
- # symbol indicates that an element is accessible only to packages contained within a given package

#### Analysis Packages

![](05_RequirementsEngineering/05_RequirementsEngineering/_page_52_Figure_1.jpeg)

# *Requirements Modeling: Behavior*

#### Behavioral Modeling

- The behavioral model indicates how software will respond to external events.
- To create the model, the analyst must perform the following steps:
  - 1. Evaluate all use-cases to fully understand the sequence of interaction within the system.
  - 2. Identify events that drive the interaction sequence and understand how these events relate to specific objects.
  - 3. Create a sequence for each use-case.
  - 4. Build a state diagram for the system.
  - 5. Review the behavioral model to verify accuracy and consistency.

#### Identifying Events with Use-Cases

- In general, an event occurs whenever the system and an actor or different parts of the system **exchange information**
- Example:

- "homeowner uses the keypad to key in a four-digit password"
  - Event: *password entered* 
    - (generated by **Homeowner**)
- "password is compared with the valid password stored in the system"
  - Event: *password compared* 
    - (recognized by **ControlPanel**)

#### State Representations

- In the context of behavioral modeling, two different characterizations of states must be considered:
  - The state of each class as the system performs its function
  - The state of the system as observed from the outside as the system performs its function
- The state of a class takes on both **passive** and **active**:
  - A *passive state* is simply the current status of all of an object's attributes
    - The passive state of the class **Player** would include the current value of position, orientation, …
  - The *active state* of an object indicates the current status of the object as it undergoes a continuing transformation
    - The active states of the class **Player**: moving, at rest, injured, being cured, trapped, lost, …
    - An event (sometimes called a trigger) must occur to force an object to make a transition from one active state to another

### State and Sequence Diagrams

- Two different behavioral representations:
  - 1. State diagram—indicates how **an individual class** changes state based on external events
    - The active state model
    - Shows the "life history" of an object
  - 2. Sequence diagram—shows **the behavior of the system** as a function of time
    - Shows how events cause transitions from one object to another object
      - (key classes in a use-case and the events that cause behavior to flow from class to class)

### State Diagram Elements

- state—active states for a class
- state transition—the movement from one state to another (represented by arrows)
- event (or trigger)—causes change between active states
  - represented by a label for the arrow
- guard—a Boolean condition that must be satisfied in order to occur the transition
- action—occurs concurrently with the state transition or as a consequence of it
  - generally involves one or more operations (responsibilities) of the object

#### State Diagram for the ControlPanel Class (use-case: "SafeHome security function")

![](05_RequirementsEngineering/05_RequirementsEngineering/_page_59_Figure_1.jpeg)

#### Sequence diagram (**partial**) for the SafeHome security function

![](05_RequirementsEngineering/05_RequirementsEngineering/_page_60_Figure_1.jpeg)

# *Requirements Modeling for Web and Mobile Apps*

#### When Do We Perform Analysis?

- In some Web/Mobile App situations, analysis and design merge. However, an explicit analysis activity occurs when …
  - the Web or Mobile App to be built is large and/or complex
  - the number of stakeholders is large
  - the number of developers is large
  - the development team members have not worked together before
  - the success of the app will have a strong bearing on the success of the business

#### Requirements Modeling for Web/Mobile Apps

- Content Analysis—identifies the full spectrum of content to be provided by the app (e.g., text, images, video, audio data,..)
- Interaction Analysis—describes the manner in which the user interacts with the app
- Functional Analysis—defines the operations that will be applied to manipulate content and describes all processing functions in detail
- Configuration Analysis—describes the environment and infrastructure in which the app resides
- Navigation Analysis—defines the overall navigation strategy for the app

#### The Content Model

- Content objects: **user-visible** entities that are created or manipulated as a user interacts with app
  - E.g., a textual description of a product, an article, a photograph, a user's response on a forum, an animated logo, a video of speech, …
- Can be extracted from use-cases
  - examine the scenario description for direct and indirect references to content
- Attributes of each content object are identified
- The relationships among content objects and/or the hierarchy of content maintained by an app
  - Relationships—entity-relationship diagram or UML
  - Hierarchy—data tree or UML

#### Example: Data Tree

- Data tree shows a hierarchy of information that describes a content object (here, product component)
- A use case, *Purchasing SafeHome Components,*  describes this scenario:
  - I will be able to get descriptive and pricing information for each product component

 In this example: There are eight content objects (shaded rectangles)

![](05_RequirementsEngineering/05_RequirementsEngineering/_page_65_Figure_5.jpeg)

#### The Interaction Model

- Web and mobile apps enable a "conversation" between an end user and the app
- This conversation can be described using an interaction model
- Composed of four elements:
  - use-cases
  - sequence diagrams
  - state diagrams
  - and/or user interface prototypes
- *In many instances, a set of use cases is sufficient to describe the interaction at an analysis level (further refinement and detail is introduced during design)*

#### Sequence Diagram

![](05_RequirementsEngineering/05_RequirementsEngineering/_page_67_Figure_1.jpeg)

Figure 18.5 Sequence diagram for use-case:*select SafeHome components*

#### State Diagram

![](05_RequirementsEngineering/05_RequirementsEngineering/_page_68_Figure_1.jpeg)

Figure 1 8 .6 Part ial st at <sup>e</sup> diagram f or **ne <sup>w</sup> <sup>c</sup> us t ome**in**r**t eract ion

#### The Functional Model

- The functional model addresses two processing elements of an app:
  - 1. user-observable functionality that is delivered by the app to end-users
    - Any processing functions that are **initiated directly by the user**
  - 2. operations contained within analysis classes that implement behaviors associated with the class
- For example, a financial mobile app might provide a financial function: computing mortgage payment
  - From the user's point of view, this is a visible process (it has a visible outcome)
  - This process may actually be implemented using different operations within analysis classes
- An activity diagram can be used to show processing flow

### Activity Diagram

An activity diagram for the *takeControlOfCamera()* operation that is part of the *Camera* analysis class used within the *Control cameras* use case

![](05_RequirementsEngineering/05_RequirementsEngineering/_page_70_Figure_2.jpeg)

### The Configuration Model

- In some cases, the configuration model is nothing more than a list of server-side and client-side attributes
- Server-side
  - Server hardware and operating system environment must be specified
  - Interoperability considerations on the server-side must be considered
  - Appropriate interfaces and communication protocols must be specified
- Client-side
  - Browser configuration issues must be identified
  - Testing requirements should be defined
- For complex apps, the UML deployment diagram can be used to model configuration architectures

### The Navigation Model

- In most mobile applications that reside on smartphone platforms:
  - Navigation is generally constrained to relatively simple button lists and icon-based menus
  - The depth of navigation is relatively shallow
  - So, navigation modeling is relatively simple
- For WebApps, navigation modeling is more complex
  - How each user category will navigate from one WebApp element (e.g., content object) to another
- The mechanics of navigation are defined at design
- At this stage, we focus on overall navigation requirements

#### Navigation Requirements

- Should certain elements be easier to reach (require fewer navigation steps) than others? What is the priority for presentation?
- How should navigation errors be handled?
- Should navigation be accomplished via links, via searchbased access, or by some other means?
- Should a navigation log be maintained for users?
- Should a full navigation map or menu (as opposed to a single "back" link) be available at every point in a user's interaction?
- Can a user "store" his previous navigation through the WebApp to expedite future usage?
- Can a user take a "guided tour" that highlight the most important available elements (content objects and functions)?

…

#### Further Reading

| PART TWO   | MODELING 103                                                       |
|------------|--------------------------------------------------------------------|
| CHAPTER 7  | Principles That Guide Practice 104                                 |
| CHAPTER 8  | Understanding Requirements 131                                     |
| CHAPTER 9  | Requirements Modeling: Scenario-Based Methods 166                  |
| CHAPTER 10 | Requirements Modeling: Class-Based Methods 184                     |
| CHAPTER 11 | Requirements Modeling: Behavior, Patterns, and Web/Mobile Apps 202 |
| CHAPTER 12 | Design Concepts 224                                                |
| CHAPTER 13 | Architectural Design 252                                           |
| CHAPTER 14 | Component-Level Design 285                                         |
| CHAPTER 15 | User Interface Design 317                                          |
| CHAPTER 16 | Pattern-Based Design 347                                           |
| CHAPTER 17 | WebApp Design 371                                                  |
| CHAPTER 18 | MobileApp Design 391                                               |
|            |                                                                    |

### *The End*



---

# سند 6: 06_DesignConcepts

**فایل اصلی:** `06_DesignConcepts.pdf`

### **Design Concepts**

#### **Modeling: Chapter 12**

*Slide Set to accompany*

*Software Engineering: A Practitioner's Approach, 8/e*

**by Roger S. Pressman and Bruce R. Maxim**

**Slides copyright © 1996, 2001, 2005, 2009, 2014 by Roger S. Pressman**

#### *For non-profit educational use only*

May be reproduced ONLY for student use at the university level when used in conjunction with *Software Engineering: A Practitioner's Approach, 8/e.* Any other reproduction or use is prohibited without the express written permission of the author.

All copyright information MUST appear if these slides are posted on a website for student use.

### Agenda

- Design Overview
- Design Concepts
- Design Models

![](06_DesignConcepts/06_DesignConcepts/_page_1_Picture_4.jpeg)

#### *Design Overview*

# Requirements, Design, and Implementation

- Requirements (Analysis) Model
  - Model of "**what** we need?"
  - Problem space
- Design Model
  - Model of "**how to** create or implement?"
  - Solution space
- Software Product (Implementations, Programs, …)
  - Actual creation (no model)

#### Software Design

- Software design encompasses the set of **principles**, **concepts**, and **practices** that lead to the development of a high-quality product.
- Design principles establish an overriding philosophy that guides you in the design work
  - E.g., The design should exhibit uniformity and integration
- Design concepts must be understood before the mechanics of design practice apply
  - E.g., modularity, pattern, …
- Design practices lead to the creation of various software models that guide the construction activity

#### Software Design Manifesto

- Mitch Kapor, presented a "software design manifesto" in *Dr. Dobbs Journal.* He said:
  - **Well-designed software programs should exhibit:**
  - *1. Firmness:* A program should not have any bugs that inhibit its function.
  - *2. Commodity:* A program should be suitable for the purposes for which it was intended.
  - *3. Delight:* The experience of using the program should be pleasurable one.

### Design and Quality

- 1. The design must cover **all the requirements**
  - Both functional and non-functional requirements
- 2. The design must be a **readable** and **understandable**
  - For those who generate code, test and subsequently support the software
- 3. The design should provide **a complete picture** of the software
  - Addressing the informationl, functional, and behavioral domains

## Design Principles

- The design process should not suffer from 'tunnel vision.'
  - There are always alternative design solutions
  - The best designers consider all (or most) of them before settling on the final design model.
- The design should be traceable to the analysis model.
- The design should not reinvent the wheel.
- The design should exhibit uniformity and integration.
- The design should be structured to accommodate change.
- Design is not coding, coding is not design.
- The design should be assessed for quality as it is being created, not after the fact.
- … *From Davis [DAV95]*

#### *Design Concepts*

#### Fundamental Concepts

- Abstraction—data and procedure
- Architecture—the overall structure of the software
- Patterns—"conveys the essence" of a proven design solution
- Separation of concerns—any complex problem can be more easily handled if it is subdivided into pieces
- Modularity—compartmentalization of data and function
- Hiding—controlled interfaces
- Functional independence—single-minded function and low coupling
- Refinement—elaboration of detail for all abstractions
- Aspects—a mechanism for understanding how global requirements affect design
- Refactoring—a reorganization technique that simplifies the design
- OO design concepts—Appendix II
- Design Classes—provide design detail that will enable analysis classes to be implemented

#### 1) Data Abstraction

 A data abstraction is a named collection of data that describes a data object.

![](06_DesignConcepts/06_DesignConcepts/_page_10_Figure_2.jpeg)

#### 2) Procedural Abstraction

- A procedural abstraction refers to the ability of naming and later calling a set of instructions.
  - The name of a procedural abstraction implies its function.
  - It is called abstraction because the caller of the procedure only needs to **know what** the procedure does, **not how** it does it.

![](06_DesignConcepts/06_DesignConcepts/_page_11_Figure_4.jpeg)

#### 3) Architecture

- Software architecture is:
  - the structure or organization of program components (modules),
  - the manner in which these components interact,
  - and the structure of data that are used by the components.

*"The overall structure of the software and the ways in which that structure provides conceptual integrity for a system." [SHA95a]*

#### What is conceptual integrity?

- Conceptual integrity is the principle that anywhere you look in your system, you can tell that the design is part of the same overall design.
- Even if multiple people work on it, it would seem cohesive and consistent as if **only one mind** was guiding the work.
  - The system reflects **one set** of design ideas, instead of containing many good but independent, conflicting and uncoordinated ideas.
  - Development teams must have in their **collective minds** the same vision for the software

#### Architectural Design

#### **There are a set of properties for an architectural design:**

- **1. Structural properties.**
  - components of a system (e.g., modules, objects)
  - and the manner in which those components are packaged and interact with one another
- **2. Extra-functional properties.** The architectural design should address how to achieve **non-functional requirements**
  - e.g., performance, reliability, security, etc
- **3. Families of related systems.** The architectural design should draw upon **repeatable patterns** that are **commonly encountered** in the design of **similar systems**.
  - The design should reuse architectural building blocks

### 4) Design Patterns

 A software design pattern is a **general**, **reusable solution** to a **commonly occurring problem** within a **certain context** in software design

#### *Design Pattern Template*

*Pattern name***—describes the essence of the pattern in a short but expressive name** 

*Intent***—describes the pattern and what it does**

*Also-known-as***—lists any synonyms for the pattern**

*Motivation***—provides an example of the problem** 

*Applicability***—notes specific design situations in which the pattern is applicable**

*Structure***—describes the classes that are required to implement the pattern**

*….*

*Different types of design patterns?*

For an example, see Slide 62 (Mediator design pattern)

### Design Pattern Examples

- Singleton
  - Ensure a class has only one instance
- Object pool
  - Avoid expensive acquisition and release of resources
- Adapter
  - Convert the interface of a class into another interface clients expect
- …

![](06_DesignConcepts/06_DesignConcepts/_page_16_Picture_9.jpeg)

![](06_DesignConcepts/06_DesignConcepts/_page_16_Picture_10.jpeg)

![](06_DesignConcepts/06_DesignConcepts/_page_16_Picture_14.jpeg)

## 5) Separation of Concerns

- A *concern* is a feature or behavior that is specified as part of the requirements
- Any complex problem can be more easily handled if it is subdivided into pieces
  - pieces that can be solved and/or optimized independently
- A problem takes less effort and time to solve:
  - By separating concerns into smaller, and therefore more manageable pieces
    - Divide-and-conquer strategy

## 6) Modularity

- Modularity is the most common manifestation of separation of concerns.
- **Monolithic** software
  - (i.e., a large program composed of a single module) cannot be easily grasped by a software engineer.
    - The overall complexity would make understanding impossible.
- You should break the design into many modules
  - hoping to make understanding easier
  - and reduce the cost required to build [and maintain] the software
- What is the risk of "many modules"?
  - **Integration**

![](06_DesignConcepts/06_DesignConcepts/_page_19_Figure_0.jpeg)

#### Modularity: Trade-offs

What is the "right" number of modules for a specific software design?

![](06_DesignConcepts/06_DesignConcepts/_page_19_Figure_3.jpeg)

## 7) Information Hiding

- Modules should be specified and designed so that:
  - information (algorithms and data) contained within a module is **inaccessible** to other modules that have **no need** for such information.

![](06_DesignConcepts/06_DesignConcepts/_page_20_Figure_3.jpeg)

## Why Information Hiding?

- reduces the likelihood of "**side effects**"
- limits the global impact of **local design decisions**
- emphasizes communication through controlled **interfaces**
- discourages the use of **global data**
- leads to **encapsulation**—an attribute of high quality design
- results in higher **quality** software

## 8) Functional Independence

- Functional independence is achieved by developing modules with "single-minded" function and a "dislike" to excessive interaction with other modules.
- *Cohesion*: The relative functional strength of a module
- *Coupling*: The relative interdependence among modules
  - Collaboration between modules should be kept to an acceptable minimum (**loosely coupled**)
  - If a design model is tightly coupled (each design class collaborates with another), the system is difficult to implement, test and maintain

#### Cohesion

- Cohesion is the degree to which elements inside a module (e.g., class, package, …) are functionally related to each other and united in their purpose
- A cohesive module
  - has a **small**, **focused** set of responsibilities
  - and **single-mindedly** applies attributes and methods to implement those responsibilities
  - performs a single task, requiring little interaction with other components in other parts of a program
- For example, all methods within class **User** should represent the user behavior
- Modules that perform many unrelated functions must be avoided

#### Cohesion: Examples

- Example 1: class **VideoClip** contains a set of data and methods for editing the video clip.
  - **VideoClip** is a cohesive class as long as:
  - 1. Each method focuses solely on attributes associated with the video clip
  - 2. All data and methods related to the video editing are incorporated in **VideoClip**
- Example 2: class **User** can be responsible for storing the email address of the user but not for validating it
  - That should belong to some other class like **Email**

![](06_DesignConcepts/06_DesignConcepts/_page_24_Picture_7.jpeg)

#### A Loosely Coupled and Highly Cohesive System

![](06_DesignConcepts/06_DesignConcepts/_page_25_Picture_1.jpeg)

#### 9) Refinement

- Stepwise refinement is a top-down design strategy.
- An application is developed by successively refining levels of procedural detail.
  - Decomposing a macroscopic statement of function in a stepwise fashion until programming language statements are reached.

A macroscopic statement of function (i.e., at a high level of abstraction)

in a **stepwise** manner

programming language statements (the lowest level of abstraction)

#### 10) Aspects

- Consider two requirements, *A* and *B*: Requirement *A crosscuts* requirement *B,* if *B* cannot be satisfied without taking *A* into account.
- Cross-cutting concerns often **cannot be cleanly decomposed** from the rest of the system

An **aspect** is a representation of a cross-cutting

concern

![](06_DesignConcepts/06_DesignConcepts/_page_27_Picture_5.jpeg)

#### 11) Refactoring

- Martin Fowler defines refactoring in the following manner:
  - "Refactoring is the process of changing a software system in such a way that it does not alter the external behavior of the code [design] yet improves its internal structure."
- When software is refactored, the existing design is examined for:
  - redundancy
  - unused design elements
  - inefficient or unnecessary algorithms
  - poorly constructed or inappropriate data structures
  - or any other design failure [bad smells] that can be corrected to yield a better design

## 12) OO Design Concepts

- Design classes
  - Entity classes
  - Boundary classes
  - Controller classes
- Inheritance—all responsibilities of a superclass is immediately inherited by all subclasses
- Messages—stimulate some behavior to occur in the receiving object
- Polymorphism—a characteristic that greatly reduces the effort required to extend the design

## Design Classes: Entity

- Entity classes are extracted directly from the problem statement
  - Also called business classes
  - e.g., **FloorPlan** and **Sensor**
  - Things that are to be stored in a database and persist
  - Analysis classes are refined during design to become entity classes
    - The analysis model defines a set of analysis classes
    - The abstraction level of an analysis class is relatively high
    - As the design model evolves, design classes refine the analysis classes by providing more details that will enable the classes to be implemented

## Analysis Class vs Design Class

![](06_DesignConcepts/06_DesignConcepts/_page_31_Figure_1.jpeg)

## Design Classes: Boundary

- Boundary classes are developed during design to create the user interface that the user sees and interacts
  - E.g., interactive screen or printed reports
  - Entity objects contain information that is important to users, but they do not display themselves
  - Boundary classes are designed with the responsibility of managing how entity objects are represented to users
  - For example: **CameraWindow**
    - This class has the responsibility of displaying surveillance camera output for the SafeHome homeowner

## Design Classes: Controller

- Controller classe*s* are designed to manage
  - the creation or update of entity objects;
  - the instantiation of boundary objects as they [controllers] obtain information from entity objects;
  - complex communication between sets of objects (i.e., coordination);
  - validation of data communicated between objects or between the user and the application.
  - In general, controller classes are not considered until the design activity has begun

#### Entity, Boundary, Controller: An Example

![](06_DesignConcepts/06_DesignConcepts/_page_34_Figure_1.jpeg)

An Example of Analysis Class Diagram vs Design Class Diagram

*Analysis Class Diagram*

#### An Example of Analysis Class Diagram vs Design Class Diagram

![](06_DesignConcepts/06_DesignConcepts/_page_36_Figure_1.jpeg)

### Design Class Characteristics

- Each design class be reviewed to ensure that it is "wellformed"
- Four characteristics of a well-formed design class:
- 1. Complete and sufficient includes **all necessary attributes and methods** and contains **only** those methods **needed** to achieve class intent (no more and no less)
- 2. Primitiveness **each class method** focuses on providing **one service**
- 3. High cohesion small, focused, single-minded classes
- 4. Low coupling class collaboration kept to minimum

## Primitiveness: An Example

- Once the service has been implemented with a method
  - The class **should not provide another way** to accomplish the **same thing**
- For example, the class **VideoClip** for video editing software
- It has attributes **startPoint** and **endpoint** to indicate the start and end points of the clip
- The methods, *setStartPoint()* and *setEndPoint()*, provide the only means for establishing start and end points for the clip.

#### *Design Model*

#### Design Model Elements

- Data elements
  - Data model --> data structures (using ER for example)
  - Data model --> database architecture
- Architectural elements
  - Application domain
  - Analysis classes, their relationships, collaborations and behaviors are transformed into design realizations
  - Architectural patterns and "styles" (Chapters 13 and 16)
- Interface elements
  - the user interface (UI) (Chapter 15)
  - external interfaces to other systems, devices, networks or other producers or consumers of information
  - internal interfaces between various design components
- Component elements
- Deployment elements

### Data Design Elements

- Focuses on the data domain
  - Data objects independently of processing
  - The structure of data
  - Indicates how data objects relate to one another

*An example of a data model (using ER)*

![](06_DesignConcepts/06_DesignConcepts/_page_41_Figure_6.jpeg)

## Architectural Design Elements

- The architectural model is usually depicted as a set of interconnected subsystems
  - often derived from analysis packages within the requirements model
- Each subsystem may have its own architecture
- The architectural model is derived from three sources:
  - 1. Information about the **application domain**
  - 2. Specific **requirements model** (the problem at hand)
    - Such as use cases or analysis classes
  - 3. The availability of **architectural patterns and styles**

(More details: next sessions)

## Interface Design Elements

- The interface design elements depict:
  - information flows into and out of a system
    - External communications
  - and how it is communicated among the components of the architecture
    - Internal communications
- Important elements
  - **User interface** (UI)
  - **External interfaces** to other systems
  - **Internal interfaces** between various design components

#### Interface Elements—UI

- UI design incorporates:
  - **aesthetic** elements (e.g., layout, color, graphics)
  - **ergonomic** elements (e.g., information layout and placement, UI navigation)
  - **technical** elements (e.g., UI patterns, reusable components)
- Details in Chapter 15

#### Interface Elements—External Interfaces

- The design of external interfaces requires information about the sender and receiver entities
- This information should be
  - collected during requirements engineering
  - and verified once the interface design commences
    - The designer should ensure that the specification for the interface is **accurate** and **complete**
- The design of external interfaces should incorporate error checking and appropriate security features.

#### Interface Elements—Internal Interfaces

- The design of internal interfaces is closely aligned with **component-level design**
  - represents all public operations and messaging schemes required to enable communication between various classes or components
- Two tasks are required:
  - 1. Specifying message details when classes or components collaborate
  - 2. Identify appropriate interfaces for each component
- Details in Chapter 14

#### 1) Designing Messaging Schema

- The design model can show the details of collaborations by specifying the structure of messages that are passed between objects within a system
- During requirements modeling, collaboration diagrams show how analysis classes collaborate with one another

#### Example:

- Three objects collaborate to prepare a print job for submission to the production stream.
- Messages are passed between objects as shown by arrows

#### *Collaboration diagram with messaging*

![](06_DesignConcepts/06_DesignConcepts/_page_47_Figure_7.jpeg)

#### 1) Designing Messaging Schema

 As design proceeds, each message is elaborated by expanding its syntax in the following manner:

- [guard condition] specifies **conditions** that must be met before the message can be sent;
- sequence expression is an integer value that indicates the sequential **order** in which a message is sent;
- (return value) is the name of the **information that is returned**  by the invoked operation
- message name identifies the invoked **operation** (e.g., buildJob);
- (argument list) is the list of **attributes passed** to the operation.

#### 2) Designing the Interface of Objects

- A UML interface is a classifier that declares a set of public operations
- The interface contains no internal structure, it has no attributes and no associations
- Two notations:

![](06_DesignConcepts/06_DesignConcepts/_page_49_Figure_4.jpeg)

*"lollipop" symbol is shorthand for a realization relationship of an interface classifier*

![](06_DesignConcepts/06_DesignConcepts/_page_49_Figure_7.jpeg)

#### An Example of Interface Representation

**ControlPanel** provides the behavior associated with a keypad

It implements the operations *readKeyStroke*() and

*decodeKey*()

 ControlPanel provides theses two services to other classes (i.e., **WirelessPDA** and **Mobilephone**)

 Interface **KeyPad** is realized (implemented) by **ControlPanel**

![](06_DesignConcepts/06_DesignConcepts/_page_50_Figure_6.jpeg)

#### Component-Level Design Elements

- Describes the **internal detail** of each software component
  - Data structures for all local data objects within a component
  - Algorithmic detail for all processing functions that occurs within a component
  - An interface that allows access to all operations (behaviors) of a component
- Details in Chapter 14

#### An Example of Component-Level Design

![](06_DesignConcepts/06_DesignConcepts/_page_52_Figure_1.jpeg)

## Component Diagram

In UML, a component is represented as follows:

![](06_DesignConcepts/06_DesignConcepts/_page_53_Picture_2.jpeg)

Provided Interface and the Required Interface:

![](06_DesignConcepts/06_DesignConcepts/_page_53_Picture_4.jpeg)

- Provided interface: An interface (or services) that the component provides
- Required interface: An interface (or services) that the component requires

![](06_DesignConcepts/06_DesignConcepts/_page_53_Picture_7.jpeg)

# Component Diagram: Example 1

![](06_DesignConcepts/06_DesignConcepts/_page_54_Figure_1.jpeg)

# Component Diagram: Example 2

![](06_DesignConcepts/06_DesignConcepts/_page_55_Figure_1.jpeg)

What is **port**?

![](06_DesignConcepts/06_DesignConcepts/_page_55_Picture_3.jpeg)

#### Deployment-Level Design Elements

- Indicates how software functionality and subsystems will be allocated within the **physical computing environment**
- Modeled using UML deployment diagrams
  - *1. Descriptor form* deployment diagrams show the computing environment but does not indicate hardware configuration details
  - *2. Instance form* deployment diagrams explicitly indicate hardware configuration details
- Developed during the latter stages of design

#### Deployment Diagram: *Descriptor Form*

- The elements of the *SafeHome* product are configured to operate within three primary computing environments:
- 1. A homebased PC
- 2. The SafeHome control panel
- 3. A server housed at CPI Corp

![](06_DesignConcepts/06_DesignConcepts/_page_57_Picture_5.jpeg)

#### Deployment Diagram: *Instance Form*

![](06_DesignConcepts/06_DesignConcepts/_page_58_Figure_1.jpeg)

#### Further Reading

| PART TWO   | MODELING 103                                                       |
|------------|--------------------------------------------------------------------|
| CHAPTER 7  | Principles That Guide Practice 104                                 |
| CHAPTER 8  | Understanding Requirements 131                                     |
| CHAPTER 9  | Requirements Modeling: Scenario-Based Methods 166                  |
| CHAPTER 10 | Requirements Modeling: Class-Based Methods 184                     |
| CHAPTER 11 | Requirements Modeling: Behavior, Patterns, and Web/Mobile Apps 202 |
| CHAPTER 12 | Design Concepts 224                                                |
| CHAPTER 13 | Architectural Design 252                                           |
| CHAPTER 14 | Component-Level Design 285                                         |
| CHAPTER 15 | User Interface Design 317                                          |
| CHAPTER 16 | Pattern-Based Design 347                                           |
| CHAPTER 17 | WebApp Design 371                                                  |
| CHAPTER 18 | MobileApp Design 391                                               |

#### *The End*

![](06_DesignConcepts/06_DesignConcepts/_page_61_Picture_0.jpeg)

#### Intent

- Mediator is a **behavioral design pattern** that lets you **reduce dependencies** between objects
- Promotes **loose coupling**

#### Solution

- Restricts direct communications between objects and forces them to collaborate only via a mediator object
- components collaborate indirectly by calling a special mediator object that redirects the calls to appropriate components
- So, the components depend only on a single mediator class instead of being coupled to dozens of their colleagues

### Mediator Design Pattern

- Each component has a reference to a mediator
- The Mediator interface declares a method for communication between components (usually a single notification method).
- Concrete mediator often keep references to all components it manage and sometimes even manages their lifecycle
- Components must not be aware of other components
- When something happens with a component, it notifies the mediator
- Mediator can easily identify the sender and decide what should be done in return (may do something on its own or pass the request to another component)

![](06_DesignConcepts/06_DesignConcepts/_page_62_Figure_7.jpeg)

#### Facade Pattern

```
64
```



---

# سند 7: 07_Refactoring

**فایل اصلی:** `07_Refactoring.pdf`

![](07_Refactoring/07_Refactoring/_page_0_Figure_0.jpeg)

**درس »مهندسی نرم افزار 2«**

**بازآرايي برنامه Code Refactoring**

![](07_Refactoring/07_Refactoring/_page_0_Picture_5.jpeg)

#### **سرفصل مطالب**

- بازآرایی کد )Refactoring Code )چيست؟
  - نياز به بازآرایی
  - مزایای بازآرایی
  - بوهای بد در کد و تکنيک های بازآرایی

## **بازآرايي )Refactoring)**

- یک فرایند منظم و منضبط برای بازسازی ساختار برنامه
  - با هدف بهبود کيفيت کد
  - بدون ایجاد تغيير در رفتار برنامه

![](07_Refactoring/07_Refactoring/_page_2_Picture_4.jpeg)

# **تعريف بازآرايي**

- تغييری در ساختار داخلی نرم افزار،
- که باعث می شود راحت تر خوانده و فهميده شود،
- و تغيير )نگهداری( آن کم هزینه تر و ساده تر شود،
- بدون این که تغييری در رفتار نرم افزار مشاهده شود.
- مهمترین فایده بازآرایی: افزایش **قابلیت نگهداری** نرم افزار

# **بازآرايي چه نمي کند؟ )کارهايي که بازآرايي نیستند(**

- تغيير در رفتار برنامه
- ایجاد امکانات جدید
  - رفع باگ
- ( معموالً( بازآرایی زمانی اتفاق می افتد که نرم افزار به درستی کار می کند

- دقت کنيد:
- در حالت عادی وقتی در حال برنامه نویسی هستيم، به یکی از کارهای فوق مشغوليم
  - و یا در حال توليد کدهای تست )آزمون واحد( هستيم
    - بازآرایی: حالتی جدید در برنامه نویسی

## **بازآرايي چه مي کند؟**

- بهبود ساختار داخلی برنامه
- اجرای فرایندی منظم برای **تمیز کردن کد**
  - بهبود طراحی برنامه بعد از نوشتن کد
  - بخصوص در فرایندهای چابک توليد نرم افزار
    - بهبود دائمی طراحی برنامه

# **فرايند بازآرايي**

- در هر مرحله، یک اشکال ساختاری در متن برنامه پيدا می کنيم
  - مثالً یک متد که زیادی طوالنی شده است
    - منظور از اشکال، باگ نيست
- هر یک از این عالئم و اشکاالت ساختاری، یک »بوی بد« در برنامه هستند
  - Bad Smells
  - هر »بوی بد«، با یک تکنيک مشخص برطرف می شود
  - تکنيک های بازآرایی )Techniques Refactoring)

#### **مثال**

- این برنامه را ببينيد
- چه اشکاالتی دارد؟
- چگونه ساختار آن را بهبود بخشيم؟

```
مثال
```

-1 اسامی نامناسب برای متغيرها

**مثال**

تکنيک تغيير نام

![](07_Refactoring/07_Refactoring/_page_10_Picture_1.jpeg)

```
-2 دسته داده ها
)تکرار گروهی از متغيرها 
     در نقاط مختلف کد(
```

```
مثال
```

 تعریف کالس مستطيل با دو متغير طول و عرض

تکنيک استخراج کالس

```
مثال
Scanner scanner = new Scanner(System.in);
System.out.println("Rectangle Info.");
System.out.print("Enter the width: ");
int width = scanner.nextInt();
System.out.print("Enter the length: ");
int length = scanner.nextInt();
Rectangle rectangle1 = new Rectangle(length, width);
System.out.println("Rectangle Info.");
System.out.print("Enter the width: ");
width = scanner.nextInt();
System.out.print("Enter the length: ");
length = scanner.nextInt();
Rectangle rectangle2 = new Rectangle(length, width);
int area1 = rectangle1.getWidth()*rectangle1.getLength();
int area2 = rectangle2.getWidth()*rectangle2.getLength();
if(area1 == area2)
      System.out.println("Equal");
                                                       بازآرایی کد اوليه بر اساس 
                                                      کالس شناسایی شده جدید
                                                              )کالس مستطيل(
                                                    قابليت استفاده مجدد از کالس 
                                                        مستطيل به تعداد دلخواه
```

```
14 مهندسی نرم افزار 2 بازآرايی برنامه
Scanner scanner = new Scanner(System.in);
System.out.println("Rectangle Info.");
System.out.print("Enter the width: ");
int width = scanner.nextInt();
System.out.print("Enter the length: ");
int length = scanner.nextInt();
Rectangle rectangle1 = new Rectangle(length, width);
System.out.println("Rectangle Info.");
System.out.print("Enter the width: ");
width = scanner.nextInt();
System.out.print("Enter the length: ");
length = scanner.nextInt();
Rectangle rectangle2 = new Rectangle(length, width);
int area1 = rectangle1.getWidth()*rectangle1.getLength();
int area2 = rectangle2.getWidth()*rectangle2.getLength();
if(area1 == area2)
      System.out.println("Equal");
```

![](07_Refactoring/07_Refactoring/_page_13_Picture_1.jpeg)

-3 قطعه کد تکراری

![](07_Refactoring/07_Refactoring/_page_14_Picture_0.jpeg)

تکنيک استخراج متد

```
Scanner scanner = new Scanner(System.in);
```

```
مثال
```

```
System.out.println("Rectangle Info.");
System.out.print("Enter the width: ");
int width = scanner.nextInt();
System.out.print("Enter the length: ");
int length = scanner.nextInt();
Rectangle rectangle1 = new Rectangle(length, width);
```

```
System.out.println("Rectangle Info.");
System.out.print("Enter the width: ");
width = scanner.nextInt();
System.out.print("Enter the length: ");
length = scanner.nextInt();
Rectangle rectangle2 = new Rectangle(length, width);
```

-4 قطعه کد تکراری

```
int area1 = rectangle1.getWidth()*rectangle1.getLength();
int area2 = rectangle2.getWidth()*rectangle2.getLength();
if(area1 == area2)
      System.out.println("Equal");
```

![](07_Refactoring/07_Refactoring/_page_16_Picture_0.jpeg)

```
تکنيک استخراج متد
```

#### **کد بازآرايي شده**

#### **مقايسه کد اولیه با کد بازآرايي شده**

#### **مرور مثال**

- کدی که به درستی کار می کرد
  - ساختار داخلی کد بهبود یافت
- در هر مرحله، یک »بوی بد« در متن برنامه پيدا کردیم
  - مثالً نامگذاری نامناسب، کد تکراری، و ...
  - هر بوی بد را با کمک یک تکنيک بازآرایی رفع کردیم
- **بازآرایی** = پيدا کردن بوی بد + رفع آن با کمک تکنيک مناسب بازآرایی

**بوهای بد در کد و تکنیک های بازآرايي** 

#### **»بوی بد« در برنامه**

- هر عالمتی که ممکن است نشان از یک مشکل عميق تر در برنامه باشد
  - خطایی در ساختار برنامه که )فعالً( ایجاد اشکال نمی کند
  - ولی در درازمدت مشکل ساز خواهد شد )ایجاد باگ، دشواری تغيير و غيره(
    - بوی بد، باگ نيست
- ولی روند توسعه و نگهداری نرم افزار را کند، سخت، پرهزینه و خطاخيز می کند
  - این اصطالح توسط Beck Kent رایج شد
    - « اگه بو ميده، عوضش کن!«
    - If it stinks, change it!
  - بوی بد کد توسط تکنيک های مشخص بازآرایی قابل رفع هستند

![](07_Refactoring/07_Refactoring/_page_21_Picture_10.jpeg)

#### **بوی بد: کد تکراری )CODE DUPLICATED)**

- قطعه کدی **یکسان** و یا **بسیار مشابه** که بيش از یک جا دیده شود
  - قطعاً یک عالمت بد است
  - تغيير در منطق این بخش، مستلزم تغيير همه تکرارهای آن است
    - رفع اشکال یکی، باید در همه انجام شود
    - در زمان برنامه نویسی، از »paste/copy »پرهيز کنيد
      - تکنيک های بازآرایی

- مثال برای جلوگيری از تکرار c\*b در این کد، باید از تکنيک استخراج متغير استفاده کنيم
- )Extract Method( متد استخراج
- )Extract Variable( متغير استخراج
  - )Extract Class( کالس استخراج

![](07_Refactoring/07_Refactoring/_page_22_Picture_11.jpeg)

#### **بوی بد: متد طوالني )METHOD LONG)**

- متدهای طوالنی به سختی فهميده می شوند
  - تغيير آن ها سخت تر است
  - یک متد با چند خط طوالنی است؟
- قانون مشخصی در این زمينه وجود ندارد )به زبان برنامه نویسی بسيار وابسته است(
- یک قاعده سرانگشتی این است که تعداد خطوط یک متد باید در حدی باشد که بدون نياز به اسکرول بر روی اسکرین قابل مشاهده باشد )مثال بين 5 تا 15 خط(
  - یک متد خوب، »کاری منسجم و مستقل« انجام می دهد،

نه چندین کار مختلف و غير مرتبط

- )high cohesion( انسجام
- )low coupling( استقالل
- تکنيک بازآرایی: )معموالً( استخراج متد

#### **بوی بد: دسته داده ها )CLUMPS DATA)**

- گروهی از داده ها که معموالً **با هم** مورد استفاده قرار می گيرند
  - مثال:ً نام، نام خانوادگی، شناسه و گذرواژه
- در یک کد ضعيف، این گروه از داده ها در نقاط مختلف کد، تکرار می شوند )معموال بدليل عادت paste/copy)
  - تکنيک بازآرایی:
  - .1 استخراج کالس: اگر داده های تکراری در داخل بدنه یک کالس یا متد استفاده شوند )مشابه مثالی که قبال درباره مستطيل دیدیم(
    - .2 معرفی شی پارامتر )Object Parameter Introduce): اگر داده های تکراری بعنوان پارامترهای یک متد پاس داده شوند.

#### **مثال از تکنیک بازآرايي »معرفي شي پارامتر« جهت رفع دسته داده ها**

- سه متغير مربوط به مختصات x، y و z معموال بصورت گروهی با هم استفاده می شوند
  - در این مثال: بعنوان پارامترهای ورودی متد AddCoords

#### **مثال از تکنیک بازآرايي »معرفي شي پارامتر« جهت رفع دسته داده ها**

- بازآرایی کد با تکنيک معرفی شی پارامتر
  - قرار دادن هر سه پارامتر ورودی در یک کالس

#### **بوی بد: کالس بزرگ )CLASS LARGE)**

- کالس بزرگ و طوالنی
- کالسی که حاوی داده ها، متدها و خطوط کد زیاد باشد.
  - یک کالس خوب، باید »منسجم و مستقل« باشد.
- تکنيک بازآرایی: استخراج کالس، استخراج subclass یا superclass

#### **بوی بد: کالس تنبل )CLASS LAZY)**

- کالسی که بسيار مختصر است
- مثال فقط یک متد دارد و به ندرت توسط دیگر کالس ها استفاده می شود
  - کوچک تر از آن است که یک کالس مستقل باشد
  - تکنيک بازآرایی: کالس درخط )Class Inline)
    - انتقال تمام فيچرهای یک کالس به کالس دیگر

![](07_Refactoring/07_Refactoring/_page_29_Picture_0.jpeg)

#### **مثال از تکنیک بازآرايي »کالس درخط«**

کالس تنبل در این کد: TelephoneNumber

![](07_Refactoring/07_Refactoring/_page_29_Figure_4.jpeg)

![](07_Refactoring/07_Refactoring/_page_29_Picture_5.jpeg)

#### **بوی بد: تعداد زياد پارامترهای يک متد )List Parameter Long)**

- مثال بيش از 3 یا 4 پارامتر برای یک متد
- تکنيک: تبدیل مجموعه پارامترها به یک شیء )Object Parameter Introduce)
  - تکنيک: فراخوانی متد به جای پاس شدن مقدار پارامتر

#### (Replace Parameter with Method Call)

**Problem:** Calling a query method and passing its results as the parameters of another method, while that method could call the query directly.

```
int basePrice = quantity * itemPrice;
double seasonDiscount = this.getSeasonalDiscount();
double fees = this.getFees();
double finalPrice = 
    discountedPrice(basePrice, seasonDiscount, fees);
```

**Solution:** Instead of passing the value through a parameter, try placing a query call inside the method body.

```
int basePrice = quantity * itemPrice;
double finalPrice = 
          discountedPrice(basePrice);
```

#### **بوی بد: حسادت به داشته های ديگران )Envy Feature)**

- کالسی که متدهای کالسی دیگر را بيش از حد فراخوانی می کند
  - متد/متدهایی که بيشتر از طرف یک کالس دیگر فراخوانی می شود
    - تکنيک: انتقال متد )Method Move)

#### **مطالعه تکمیلي: ساير بوهای بد در کد**

- Alternative Classes with Different Interfaces
- Incomplete Library Class
- Data Class
- Refused Bequest
- Comments
- Metaprogramming Madness
- Disjointed API
- Repetitive Boilerplate

- Primitive Obsession
- Switch Statements
- Parallel Inheritance Hierarchies
- Speculative Generality
- Temporary Field
- Message Chains
- Middle Man
- Inappropriate Intimacy

برای مطالعه بيشتر به این آدرس رجوع کنيد:

<https://refactoring.guru/refactoring/smells>

# **تکنیک های بازآرايي**

- تغيير نام )Rename)
  - کالس، متد، متغير
- )Extract Method( متد استخراج
  - )Extract Class( کالس استخراج
    - )Inline Class( درخط کالس
      - برعکس تکنيک استخراج کالس
    - )Inline Method( درخط متد
- جایگزین کردن فراخوانی یک متد با بدنه آن متد و حذف متد مربوطه
  - برعکس تکنيک استخراج متد

![](07_Refactoring/07_Refactoring/_page_34_Picture_0.jpeg)

## **مثال از تکنیک بازآرايي »متد درخط«**

مثال: امتيازدهی به یک راننده پيک تحویل غذا بر اساس تعداد

```
دفعات تاخير در تحویل
متد ...moreThan را صدا می زند. اگر نتيجه true باشد، امتياز 2 و در غير اینصورت مقدار 1 را بر می گرداند
                  اگر تعداد دفعات تاخير بيش از 5 مرتبه باشد، true و در غير اینصورت false بر می گرداند
```

![](07_Refactoring/07_Refactoring/_page_34_Picture_4.jpeg)

```
حذف متد ...moreThan و جایگزینی بدنه آن به جای فراخوانی متد
```

#### **تکنیک انتقال )MOVE)**

- انتقال کالس، متد، متغير
- به یک کالس یا بسته )package )دیگر

مثال:

#### **تکنیک باال کشیدن متد )METHOD UP PULL)**

![](07_Refactoring/07_Refactoring/_page_36_Picture_1.jpeg)

## **تکنیک پايین آوردن متد )METHOD DOWN PULL)**

![](07_Refactoring/07_Refactoring/_page_37_Picture_1.jpeg)

# **تکنیک های بازآرايي**

![](07_Refactoring/07_Refactoring/_page_38_Picture_2.jpeg)

#### **تبديل SWITCH به چندريختي )POLYMORPHISM)**

جمالت پيچيده switch یا جمالت تو در تو if

```
 قبل از بازآرایی:
class Bird {
 // ...
 double getSpeed() {
  switch (type) {
   case EUROPEAN:
    return getBaseSpeed();
   case AFRICAN:
    return getBaseSpeed() - getLoadFactor() * numberOfCoconuts;
   case NORWEGIAN_BLUE:
    return (isNailed) ? 0 : getBaseSpeed(voltage);
  }
  throw new RuntimeException("Should be unreachable");
 }
}
```

### **تبديل SWITCH به چندريختي )POLYMORPHISM)**

```
abstract class Bird {
 // ...
 abstract double getSpeed();
}
class European extends Bird {
 double getSpeed() {
  return getBaseSpeed(); }
}
class African extends Bird {
 double getSpeed() {
  return getBaseSpeed() - getLoadFactor() * numberOfCoconuts; }
}
class NorwegianBlue extends Bird {
 double getSpeed() {
  return (isNailed) ? 0 : getBaseSpeed(voltage); }
}
// Somewhere in client code
speed = bird.getSpeed();
                                                                            پس از بازآرایی:
```

#### **معرفي شيء پارامتر )OBJECT PARAMETER INTRODUCE)**

![](07_Refactoring/07_Refactoring/_page_41_Picture_3.jpeg)

 وقتی که تعدادی پارامتر معموالً همراه هم پاس می شوند

 مثال پارامترهای تاریخ شروع و تاریخ پایان در این مثال

#### **ساير تکنیک های بازآرايي**

- برای مطالعات بيشتر، به آدرس های زیر رجوع کنيد:
- 1. <http://refactoring.com/catalog/>

![](07_Refactoring/07_Refactoring/_page_42_Picture_3.jpeg)

- کاتالوگی از تکنيک های بازآرایی
- گردآوری شده توسط مارتين فاولر

2. <https://refactoring.guru/refactoring/techniques>

![](07_Refactoring/07_Refactoring/_page_43_Picture_0.jpeg)

**مطالب تکمیلي**

#### **استعاره دو کاله**

- در هنگام برنامه نویسی، زمان خود را به دو بخش **مجزا** تقسيم کنيد:
  - توليد برنامه
    - بازآرایی

![](07_Refactoring/07_Refactoring/_page_44_Picture_4.jpeg)

- در هنگام توليد برنامه، درگير بازآرایی نشوید
- در هنگام بازآرایی، امکانات جدید ایجاد نکنيد
- شاید به کرّات و به سرعت، بين این دو حالت نقش عوض کنيد
  - اما هر نقش باید به طور مستقل ایفا شود
  - در هنگام ایفای یک نقش، نقش دیگر را بازی نکنيد

![](07_Refactoring/07_Refactoring/_page_44_Picture_10.jpeg)

![](07_Refactoring/07_Refactoring/_page_44_Picture_11.jpeg)

#### **پشتیباني از بازآرايي در محیط های توسعه**

- محيط های یکپارچه توسعه )IDE )امکاناتی برای بازآرایی ارائه می کنند
- Eclipse, IntelliJ IDEA, NetBeans, …
  - اجرای تکنيک های بازآرایی را خودکار می کنند
    - اشتباهات انسانی را کاهش می دهند
    - و اجرای تکنيک ها را تسریع می بخشند
  - البته دانش، و مهارت بازآرایی هم بسيار مهم است
    - بازآرایی یک فرایند کامالً خودکار نخواهد بود
  - انتخاب اشکال )بوی بد(، تکنيک بازآرایی و نحوه اجرای تکنيک: بر عهده برنامه نویس
    - ابزارها فقط کمک می کنند

# **مثال: پشتیباني Eclipse از بازآرايي**

| Ē | /**                        | Navigate               | •             | 7                                                   |
|---|----------------------------|------------------------|---------------|-----------------------------------------------------|
|   | * Session s  * here to rep | Show Javadoc           | Alt+F1        | tion. Create properties<br>be made available across |
|   | * multiple HT              | Find Usages            | Alt+F7        | ser.                                                |
|   | *                          | Refactor               | <b>•</b>      | Rename Ctrl+R                                       |
|   | * An instan                | Format                 | Alt+Shift+F   | Move                                                |
|   | * the first ti             | Fix Imports            | Ctrl+Shift+I  | Copy                                                |
|   | * or method bi             | Insert Code            | Alt+Insert    | Safe Delete                                         |
|   | * this class.<             |                        |               | Change Method Parameters                            |
|   | *                          | Reverse Engineer       |               | Encapsulate Fields                                  |
|   | * @author Mike             | Run File               | Shift+F6      | Pull Up                                             |
| - | public class Se            | Debug File             | Ctrl+Shift+F5 | Push Down                                           |
| + | Managed Cor                | Run Into Method        | Shift+F7      | Extract Interface                                   |
|   | String answ                | New Watch              | Ctrl+Shift+F7 | Extract Superclass                                  |
|   | / * *                      | Toggle Line Breakpoint | Ctrl+F8       | Use Supertype Where Possible                        |
|   | * Const                    | Profiling              | •             | Move Inner to Outer Level                           |
| L | */                         | Cut                    | Ctrl+X        | Introduce Variable                                  |
| 早 | public Sess                | Сору                   | Ctrl+C        | Introduce Constant                                  |
|   |                            | Paste                  | Ctrl+V        | Introduce Field                                     |
|   | }                          |                        |               | Introduce Method                                    |
|   |                            | Code Folds             | •             | Convert Anonymous to Inner                          |
|   | / * *                      | Select in              | <b>b</b>      | , , , , , , , , , , , , , , , , , , ,               |

# **زمان بازآرايي**

- وقتی امکانات جدیدی به برنامه اضافه می کنيد
  - وقتی یک باگ را برطرف می کنيد
- همين طور که مرور کد )review code )می کنيد
- و البته وقتی که ابزارهای تحليل کد، اشکاالتی را گزارش می کنند

#### **ريسک بازآرايي**

![](07_Refactoring/07_Refactoring/_page_48_Picture_1.jpeg)

- بازآرایی، ذاتاً مخاطره آميز )Risky )است
- زیرا برنامه ای را تغيير می دهد که کار می کند
- ممکن است بازآرایی به ایجاد باگ های جدید منجر شود
  - چطور مدیر را برای چنين کاری متقاعد کنيم؟
    - پيشنهاد مارتين فاولر:
    - اگر مدیر شما یک فرد فنی نيست،
    - الزم نيست به مدیر بگویيد یا اجازه بگيرید!
- بازآرایی، **بخشی از کار شماست** و **در تخمین زمان لحاظ می شود**
  - زمانی که صرف بازآرایی شده، توليد آینده شما را تسریع می کند

### **مهار خطر بازآرايي**

- انجام بازآرایی به صورت سيستماتيک
  - استفاده از ابزارها و امکانات IDE
    - انجام قدم های کوچک
      - استفاده از تست
    - کنترل دائمی کيفيت
- ترسو نباشيد: »شجاعت« هم الزم است
  - پنج ارزش در XP:
  - .1 تعامل )ارتباطات(
    - .2 سادگی
- .3 بازخورد )فيدبک از سيستم، از مشتری، از تيم(
  - .4 شجاعت
    - .5 احترام

# مخالفان بازآرایی

- دلایلی که بر ضد بازآرایی میآورند
- وقت نداریم، پروژه از زمانبندی عقب است!
  - زمان زیادی برای بازآرایی هدر می رود
    - بازآرایی، کار و وظیفه من نیست

![](07_Refactoring/07_Refactoring/_page_50_Picture_5.jpeg)

- نالههایی آشنا که گاهی در مخالفت با دیگر بایدها نیز گفته میشود
  - به خصوص درباره تست و آزمون واحد
    - عدم انجام بازآرایی: وام فنی

#### **جايگاه بازآرايي در متدولوژی های چابک**

- بخشی مهم از متدولوژی های چابک
  - XP مثل
  - در کنار موضوعات دیگری مانند
    - آزمون واحد
      - مرور کد
    - برنامه نویسی دونفری
- متدولوژی های چابک، تغيير را می پذیرند
- تغيير در طراحی، تغيير در نيازمندی، تغيير در ساختار کد و ...
  - بازآرایی بخشی جدانشدنی از متدولوژی های چابک است

# **تأثیر بازآرايي در کارايي )PERFORMANCE)**

- برخی به بازآرایی انتقاد می کنند که:
- تکنيک های بازآرایی باعث می شود کارایی برنامه کاهش پيدا کند
  - مثالً تعداد متدها و فراخوانی متدها بيشتر می شود
  - یا تعداد متغيرها و فضای حافظه اشغالی بيشتر می شود
- در واقع برخی از تکنيک های بازآرایی کارایی را افزایش هم می دهند
  - تأثير بقيه تکنيک ها هم در کارایی معموالً ناچيز است
- فایده بازآرایی: ساختار کد **قابل بهبود** می شود )مثالً از نظر کارایی(
- توصيه مهم: ابتدا نرم افزاری قابل بهبود بنویسيد )با استفاده از بازآرایی(،
  - سپس در صورت لزوم آن را برای رسيدن به کارایی بهتر بهبود بخشيد
- Write tunable software first and then tune it for sufficient speed

#### بازآرایی برای انطباق با الگوهای طراحی

Anti-Pattern Examples?

- تفاوت «بوی بد» و پادالگو (anti pattern)
  - الگوهای طراحی مفاهیم سطح بالاتری هستند
- معمولاً: عدم تشخيص پادالگوها توسط ابزارهای خودکار (مثل Sonar)
- معمولاً: عدم پشتیبانی از بازآرایی پادالگوها توسط محیطهای توسعه (مثل Eclipse)
- معمولاً: در تشخیص محل استفاده از الگوی نرمافزاری، تجربه و مهارت بیشتری لازم است
  - گاهی هم این مفاهیم همپوشانی دارند: Large Class و God Object
    - معنای refactoring to patterns
    - بازآرایی به منظور رعایت الگوهای طراحی
    - گاهي: سرعت برنامهنويسي و سرعت تغييرات←عدم رعايت الگوهاي طراحي
      - وگاهی به دلیل پرهیز از over-engineering
        - نیاز به بازنویسی و بازآرایی
        - Refactoring to Patterns کتاب

#### **تحلیل استاتیک کد**

![](07_Refactoring/07_Refactoring/_page_55_Picture_0.jpeg)

- **Refactoring**: Improving the Design of Existing Code
  - Martin Fowler, Kent Beck, John Brant, William Opdyke, Don Roberts
    - کتابی قدیمی، ولی همچنان زنده و پرخواننده
      - برخی صفحات مفيد:

- [http://en.wikipedia.org/wiki/Code\\_refactoring](http://en.wikipedia.org/wiki/Code_refactoring)
- <http://refactoring.com/>
- <http://refactoring.com/catalog/>
- <http://sourcemaking.com/refactoring>
- <https://refactoring.guru/refactoring>

![](07_Refactoring/07_Refactoring/_page_56_Picture_0.jpeg)

**پايان**

#### **ضد الگوی Blob يا Object God**

- یک ضد الگو یا راه حل نادرست در طراحی یک کالس این است که مسئوليت های زیاد و بی ربط به آن بدهيم.
- به طور خالصه، اگر در ساخت یک برنامه شی گرا**، کالسی** داشته باشيد که **کارهای بسیار زیادی را به صورت انحصاری** انجام دهد، ضد الگو Blob رخ داده است.
  - این ضد الگو به Class God نيز معروف است.
    - مثال:
- فرض کنيد یک برنامه دارید که عمليات مختلفی، مانند آپلود تصاویر، نمایش تصاویر، مدیریت خطاها، تعيين سطح دسترسی کاربران به تصاویر خاص و... را انجام می دهد.
- حال فرض کنيد یک کالس بسيار بزرگ دارید که تمامی این کارها توسط توابع این کالس به صورت انحصاری انجام می شود. در واقع این جا یک **کالس Blob** ایجاد شده است که مسئوليت بيش از حد را پذیرفته است.

#### **ضد الگوی جريان گدازه يا code Dead**

- یک ضد الگو یا راه حل نادرست در انجام پروژه های تحقيقاتی این است که کدهای D&R بدون پاالیش و استانداردسازی عينا در محصول نهایی قرار گيرد.
- رفته رفته با یک کد بسيار پيچيده و پر از code-Dead مواجه می شویم که تغيير دادن آن بسيار سخت است.
- ویژگی اصلی پروژههای تحقيقاتی این است که نياز به تحقيق و توسعه (D&R (بيشتری نسبت به سایر پروژههای برنامهنویسی دارند. در این پروژهها معموال کدهایی نوشته میشود که پيچيدگی باالیی و در عين حال مستندسازی بسيار اندکی دارند.
  - کدها، کالسها و متدهای پيچيده
  - معموال افرادی که بعدا به پروژه اضافه میشوند به سختی از کدها سر در می آورند
- این کدها معموال دستکاری هم نمی شوند، زیرا ترس آن میرود که با تغيير کد، قسمتی از برنامه از کار بيفتد.

#### **ضد الگوی جريان گدازه يا code Dead**

- با بزرگتر شدن این دست از پروژهها، کدهای تحقيقاتی مانند یک سری گدازه، که به مرور زمان سفت و محکم شدهاند، در سرتاسر پروژه نفوذ می کنند و ضد الگو جریان گدازهها رخ میدهد.
- این گدازهها که سفت و محکم شدهاند، قابل تغيير نيستند و کسی هم از آنها سر در نمی آورد. مخصوصا اگر برنامهنویسان اصلی این گدازهها از پروژه جدا شده باشند.
  - به طور خالصه:
- ضد الگو جریان گدازهها معموال زمانی رخ می دهد که پروژه )یا قسمتی از آن( بر پایه تحقيقات شروع شده ولی در نهایت کدهای تحقيقاتی به صورت یک محصول واقعی تمام شود.
  - راه حل اصلی غلبه بر این ضد الگو:
  - پاالیش کدهای تحقيقات و توسعه مطابق با معماری و استانداردهای پروژه
- کدهایی که در هنگام تحقيق و توسعه نوشته شدهاند، پاکسازی شده و کدهای استاندارد با معماری پروژه، در محصول نهایی قرار گيرد.



---

# سند 8: 08_SoftwareArchitecture

**فایل اصلی:** `08_SoftwareArchitecture.pdf`

### **Architectural Design**

#### **Modeling: Chapter 13**

*Slide Set to accompany*

*Software Engineering: A Practitioner's Approach, 8/e* **by Roger S. Pressman and Bruce R. Maxim**

**Slides copyright © 1996, 2001, 2005, 2009, 2014 by Roger S. Pressman**

#### *For non-profit educational use only*

May be reproduced ONLY for student use at the university level when used in conjunction with *Software Engineering: A Practitioner's Approach, 8/e.* Any other reproduction or use is prohibited without the express written permission of the author.

All copyright information MUST appear if these slides are posted on a website for student use.

## Agenda

- Software Architecture
- Architecture Genres and Styles
- Architectural Design

![](08_SoftwareArchitecture/08_SoftwareArchitecture/_page_1_Picture_4.jpeg)

## *Software Architecture*

### What is Architecture?

- The structure of the system,
  - which comprise software **components**,
  - the externally visible **properties** of those components,
  - and the **relationships** among them
- It is a representation that enables a software engineer to:
  - 1. analyze the effectiveness of the design in meeting its stated requirements,
  - 2. consider architectural alternatives when making design changes, and
  - 3. reduce the risks associated with the construction of the software.

#### Why is Architecture Important?

- Representations of software architecture are an enabler for communication between all parties (stakeholders)
- The architecture highlights early design decisions that will have a profound impact on all software engineering work that follows and, as important, on the ultimate success of the system
- Architecture "constitutes a relatively small, intellectually graspable mode of how the system is structured and how its components work together" [BAS03].

### Architectural Descriptions

- Architectural description is a **set of work products** that reflect **different views** of the system
- The IEEE Standard defines an *architectural description* (AD) as a "a collection of products to document an architecture."
  - The description represents multiple views, where each *view* is "a representation of a whole system from the perspective of a related set of [stakeholder] concerns."

### Architectural Decisions

- Each view of an architectural description addresses a specific stakeholder concern
- To develop each view,
  - the architect considers a **variety of alternatives**
  - and ultimately decides on the specific architectural features that **best meet** the concern

#### A Sample Architecture Decision Template

Info

#### **Architecture Decision Description Template**

Each major architectural decision can be documented for later review by stakeholders who want to understand the architecture description that has been proposed. The template presented in this sidebar is an adapted and abbreviated version of a template proposed by Tyree and Ackerman [Tyr05].

**Design issue:** Describe the architectural design

Resolution:

**Category:** 

**Assumptions:** 

issues that are to be addressed. State the approach you've chosen

to address the design issue.

Specify the design category that the issue and resolution address

(e.g., data design, content structure, component structure,

integration, presentation). Indicate any assumptions that

helped shape the decision.

Constraints: Specify any environmental

constraints that helped shape the decision (e.g., technology standards, available patterns,

project-related issues).

Alternatives:

Briefly describe the architectural design alternatives that were

considered and why they were

rejected.

**Argument:** State why you chose the

resolution over other alternatives.

**Implications:** Indicate the design

consequences of making the

decision. How will the resolution affect other architectural design

issues? Will the resolution

constrain the design in any way?

Related decisions: What other documented decisions

are related to this decision?

**Related concerns:** What other requirements are

related to this decision?

Work products: Indicate where this decision will

be reflected in the architecture

description.

**Notes:** Reference any team notes or

other documentation that was used to make the decision.

These slides are designed to accompany *Software Engineering: A Practitioner's Approach, 8/e* (McGraw-Hill, 2014). Slides copyright 2014 by Roger Pressman.

## *Architectural Genres & Styles*

### Architectural Genres

- *Genre* implies a **specific category** within the overall software domain
  - Also called an application domain
  - The architectural genre will often dictate the specific architectural approach to the structure
- Grady Booch suggests the following architectural genres for software systems:
  - artificial intelligence, communications, financial, games, industrial, medical, military, transportation, …
- A number of different **architectural styles** may be applicable to a specific genre

## Architectural Styles

- An architectural style describes:
  - 1. a **set of components** (e.g., a database, computational modules) that perform a function required by a system,
  - 2. a **set of connectors** that enable "communication, coordination and cooperation" among components,
  - **3. constraints** that define how components can be integrated to form the system, and
  - **4. semantic models** that enable a designer to understand the overall properties of a system by analyzing the known properties of its constituent parts.

#### A Brief Taxonomy of Architectural Styles

- Data-centered architectures
- Data flow architectures
- Call and return architectures
- Object-oriented architectures
- Layered architectures

#### Data-Centered Architecture

- A data store (e.g., a file or database) resides at the center
- The data store is accessed frequently by other components (clients)
  - To update, add, delete, or modify data within the store
- 1. Passive repository
  - Client software accesses the data independent of any changes to the data or the actions of other clients
- 2. Blackboard repository
  - sends notifications to client when data changes
  - blackboard component coordinates the transfer of information between clients

![](08_SoftwareArchitecture/08_SoftwareArchitecture/_page_12_Picture_9.jpeg)

#### Data-Centered Architecture: 1) Repository Architecture Style

- The data store is passive
- The clients (software components) of the data store are active, which control the logic flow
- The client sends requests to the system to perform actions (e.g. insert data), and the computational processes are independent
- The participating components check the data-store for changes
- This approach is widely used in DBMS, library information system, and CASE environments

# Data-Centered Architecture: 2) Blackboard Architecture Style

- The data store is active and its clients are passive
- The logical flow is determined by the data store
  - The flow is determined by the current data status in the data store
- It has a blackboard component, acting as a central data repository
- The data-store alerts the clients whenever there is a data-store change
- This approach is found in certain AI applications and complex applications, such as speech recognition, image recognition, security system, and business resource management systems etc.

#### Data-Centered Architecture

- Data-centered architectures promote *integrability* [Bas03].
- That is, existing components can be changed and new client components added to the architecture without concern about other clients
  - because the client components operate independently
- In addition, data can be passed among clients using the blackboard mechanism
- Client components independently execute processes

#### Data-Flow Architecture-I

- Applied when input data are to be transformed into output data through a series of computational or manipulative components
- A pipe-and-filter pattern has a set of components, called filters, connected by pipes that transmit data from one component to the next
- Each filter works independently of those components upstream and downstream
  - expect data input of a certain form
  - produces data output (to the next filter) of a specified form

![](08_SoftwareArchitecture/08_SoftwareArchitecture/_page_16_Figure_6.jpeg)

#### Data-Flow Architecture-II

- The data enters into the system and then flows through the modules one at a time until they are assigned to some final destination (output or a data store)
- The connections between the components may be implemented as I/O stream, I/O buffer, or other types of connections
- Suitable for applications that involve a well-defined series of independent data transformations or computations on orderly defined input and output (such as compilers and business data processing applications)
- Two types of execution sequences between modules
  - Batch sequential
  - Pipe and filter or non-sequential pipeline mode

#### Data-Flow Architecture: 1) Batch Sequential Architecture

- A data transformation subsystem can initiate its process only after its previous subsystem is **completely** through
- A batch of data as a whole from one subsystem to another
- The communications between the modules are conducted through temporary intermediate files which can be removed by successive subsystems
- Typical application of this architecture includes business data processing such as banking

![](08_SoftwareArchitecture/08_SoftwareArchitecture/_page_18_Figure_5.jpeg)

#### Data-Flow Architecture: 2) Pipe and Filter Architecture

- This approach lays emphasis on the incremental transformation of data by successive component
- The connections between modules are data stream which is first-in/first-out buffer
  - can be stream of bytes, characters, or any other type of such kind
- The main feature of this architecture is its concurrent and incremented execution
- Example of pipe and filter architectural style can be found in compilers
  - consecutive filters perform lexical analysis, parsing, semantic analysis, and

![](08_SoftwareArchitecture/08_SoftwareArchitecture/_page_19_Figure_7.jpeg)

### Call and Return Architecture-I

- Enables you to achieve a program structure that is relatively easy to modify and scale
- A number of substyles within this category:
  - 1. Main program/subprogram architectures
    - This classic program structure decomposes function into a control hierarchy where a "main" program invokes a number of program components, which in turn may invoke still other components
  - 2. Remote procedure call architectures
    - The components of a main program/subprogram architecture are distributed across multiple computers on a network

### Call and Return Architecture-II

![](08_SoftwareArchitecture/08_SoftwareArchitecture/_page_21_Picture_1.jpeg)

### Object-Oriented Architecture

- The components of a system encapsulate data and the operations that must be applied to manipulate the data
- Communication and coordination between components are accomplished via message passing

*A UML communication diagram that shows the message passing for the login portion of a system using an objectoriented architecture*

![](08_SoftwareArchitecture/08_SoftwareArchitecture/_page_22_Figure_4.jpeg)

#### Layered Architecture

- A number of different layers are defined, each accomplishing operations that progressively become closer to the machine instruction set
- User interface layer

 At the outer layer, components service user interface operations

Application layer

 provides application software functions

- Utility layer
  - provides utility services
- Core layer
  - At the inner layer, components perform operating system interfacing

![](08_SoftwareArchitecture/08_SoftwareArchitecture/_page_23_Picture_10.jpeg)

### The MVC Architecture-I

- The model-view-controller (MVC) architecture
- Often used in WebApp design
- A three-layer design architecture that decouples the user interface from the WebApp functionality & content
- Model
  - contains all **application-specific content** and processing **logic**
- View
  - contains all **interface-specific** functions and enables the presentation of content and processing logic to the user
- Controller
  - **manages access** to the model and the view and **coordinates** the flow of data between them
- In a WebApp, "the view is updated by the controller with data from the model based on user input" [WMT02]

### The MVC Architecture-II

![](08_SoftwareArchitecture/08_SoftwareArchitecture/_page_25_Figure_1.jpeg)

# The MVC Architecture-III

![](08_SoftwareArchitecture/08_SoftwareArchitecture/_page_26_Picture_1.jpeg)

- User requests are handled by the controller
- The controller also selects the view object that is applicable based on the user request
- Once the type of request is determined, a behavior request is transmitted to the model, which implements the functionality or retrieves the content required to accommodate the request
- The model object can access data stored in a database
- The data developed by the model must be formatted and organized by the appropriate view object
- And then transmitted from the application server back to the client-based browser for display on the customer's machine

### Architectural Patterns

- A pattern is a recurring solution to a recurring problem
- Architectural patterns address an application-specific problem within a specific context
  - The pattern proposes an architectural solution that can serve as the basis for architectural design
- They solve the problems related to the architectural style
  - For example:
  - *"What classes will we have and how will they interact, in order to implement a system with a specific set of layers"*
  - *"What high-level modules will have in our Service-Oriented Architecture and how will they communicate"*
- Examples of Architectural Patterns:
  - 3-tier, Microkernel, MVC, …

#### Architectural Style vs Architectural Pattern

- Style is a **concept**, theory (and how it's implemented is up to you)
- An architectural pattern describes a **solution** for implementing a style
  - At the level of subsystems or modules and their relationships
- For example, the overall architectural style for an application might be call-and-return or layered
  - But within that style, you will encounter a set of common problems that might best be addressed with specific architectural patterns
    - Such as: operating system process management pattern, task scheduler pattern, database management system (DBMS) pattern, …

## *Architectural Design*

## Architectural Design

- The software must be placed into **context**
- As architectural design begins, context must be established
  - Define the **external entities** (other systems, devices, people) that the software interacts with and the nature of the interaction
- This information can generally be acquired from the requirements model
- Architectural Context Diagram (ACD)
  - models the manner in which software interacts with entities external to its boundaries

# Architectural Context Diagram

- **Superordinate systems**—those systems that use the target system as part of some higher-level processing scheme
- **Subordinate systems**—those systems that are used by the target system and provide data or processing that are necessary to complete target system functionality
- **Peer-level systems**—those systems that interact on a peer-to-peer basis (i.e., information is either produced or consumed by the peers and the target system)
- **Actors**—entities (people, devices) that interact with the target system by producing or consuming information
- Each of these external entities communicates with the target system **through an interface**  (the small shaded rectangles)

![](08_SoftwareArchitecture/08_SoftwareArchitecture/_page_31_Picture_6.jpeg)

#### ACD For the SafeHome security function

![](08_SoftwareArchitecture/08_SoftwareArchitecture/_page_32_Picture_1.jpeg)

# Architectural Design (cont.)

- Once context is modeled and all external software interfaces have been described,
  - a set of architectural archetypes should be identified
- An *archetype* is an abstraction (similar to a class) that represents one element of system behavior
- The set of archetypes provides a collection of abstractions to model the **high-level architectural structure**
  - But the archetypes themselves do not provide enough implementation detail
- The designer specifies the structure of the system by defining and refining software components that implement each archetype
- This process continues iteratively until a complete architectural structure has been derived

## Defining Archetypes

- Abstract building blocks of an architectural design
- In general, a relatively small set of archetypes is required to design even relatively complex systems
- The target system architecture is composed of these archetypes,
  - which represent stable elements of the architecture
  - but may be instantiated many different ways based on the behavior of the system
- Archetypes can be derived by examining the analysis classes defined as part of the requirements model

### Archetypes Example:

#### UML relationships for SafeHome security function archetypes

- **Node:** Represents a cohesive collection of input and output elements of the home security function
  - For example, a node might be composed of (1) various sensors and (2) a variety of alarm (output) indicators
- **Detector:** An abstraction that encompasses all sensing equipment that feeds information into the target system
- **Indicator:** An abstraction that represents all mechanisms for indicating an alarm condition
  - e.g., alarm siren, flashing lights, bell, ...

![](08_SoftwareArchitecture/08_SoftwareArchitecture/_page_35_Picture_7.jpeg)

## Archetypes Example:

#### UML relationships for SafeHome security function archetypes

- **Controller:** An abstraction that depicts the mechanism that allows the arming or disarming of a node
  - If controllers reside on a network, they have the ability to communicate with one another
- Each of these archetypes is depicted using UML notation
- Recall that the archetypes form the basis for the architecture
  - but are abstractions that must be further refined as architectural design proceeds
  - For example, **Detector** might be refined into a class hierarchy of sensors

![](08_SoftwareArchitecture/08_SoftwareArchitecture/_page_36_Picture_8.jpeg)

#### Refining the Architecture into Components

- How to choose software components?
- Two sources for the derivation and refinement of components:
  - 1. The application domain (i.e., analysis classes)
  - 2. The infrastructure domain
    - The architecture must accommodate many infrastructure components that enable application components but have no business connection to the application domain
    - For example:
      - memory management components, communication components, database components, and task management components are often integrated into the software architecture

#### Component Structure: An Example

- **Top-level components** for the SafeHome home security function:
  - External communication management—coordinates communication of the security function with external entities such as other Internet-based systems
  - Control panel processing—manages all control panel functionality
  - Detector management—coordinates access to all detectors attached to the system
  - Alarm processing—verifies and acts on all alarm conditions
- *Note*
  - *Each of these top-level components should be elaborated iteratively and then positioned within the overall architecture*
  - *Design classes should be defined for each*

#### Component Structure: An Example

#### **Overall architectural structure for** *SafeHome* **with top-level components**

![](08_SoftwareArchitecture/08_SoftwareArchitecture/_page_39_Figure_2.jpeg)

#### Describing Instantiations of the System

- The architectural design to this point is still relatively **high level**
- The **major software components** have been identified
- However, **further refinement** is still necessary (recall that all design is iterative)
- To accomplish this, an actual instantiation of the architecture is developed
  - **Component elaboration**

## Refined Component Structure

![](08_SoftwareArchitecture/08_SoftwareArchitecture/_page_41_Figure_1.jpeg)

### Architectural Considerations

- Economy The best architecture is uncluttered and relies on a proper abstraction level to reduce unnecessary detail
- Visibility Architectural decisions and the reasons for them should be obvious to software engineers who examine the model at a later time
- Spacing Separation of concerns in a design without introducing hidden dependencies
  - Too much spacing leads to fragmentation
  - Domain-driven design can help to identify what to separate in a design and what to treat as a coherent unit
- Symmetry Architectural symmetry implies that a system is consistent and balanced in its attributes
  - Example: a *customer account* object with both *open()* and *close()* methods
- Emergence Emergent, self-organized behavior and control

### ADL

- *Architectural Description Language* (ADL) provides a semantics and syntax for describing a software architecture
- Provide the designer with the ability to:
  - decompose architectural components
  - compose individual components into larger architectural blocks and
  - represent interfaces (connection mechanisms) between components.

### Some Important ADLs

### Architecture Reviews

- A type of specialized **technical review**
- Assess the ability of the software architecture to meet the system's quality requirements (e.g., scalability or performance) and identify potential risks
- Involve only **software engineering team** members supplemented by **independent experts**
- Have the potential to reduce project costs by detecting design problems early
- The most common architectural review techniques:
  - experience-based reasoning
  - prototype evaluation
  - scenario reviews
  - checklists

#### Pattern-Based Architecture Review

- A **lightweight** architectural review process known as PBAR
  - The best option in situations in which short build cycles, volatile requirements, and/or small teams are the norm
- A face-to-face audit meeting involving architecture experts
  - Scheduled after the first working prototype or a baseline architecture is completed
- PBARs are well-suited to small, agile teams and require a relatively small amount of extra project time and effort

### PBAR Steps

- 1. Identify and discuss the most important quality attributes by walking through the relevant use cases.
- 2. Discuss a diagram of system's architecture in relation to its requirements.
- 3. Identify the architecture patterns used and match the system's structure to the patterns' structure.
- 4. Use existing documentation and use cases to examine each pattern's effect on quality attributes.
- 5. Identify and discuss all quality issues raised by architecture patterns used in the design.
- 6. Develop a short summary of issues uncovered during the meeting and make revisions to the architecture.

# Agility and Architecture-I

- Most agile developers agree that it is important to focus on software architecture when a system is **complex**
  - i.e., a product has a large number of requirements, many stakeholders, or wide geographic distribution
  - When the wrong architecture is chosen, we encounter quality problems and so the rework is required
- To avoid rework, user stories are used to create and evolve an architectural model (**walking skeleton**)

# Agility and Architecture-II

- Software architects contributes **architectural user stories**  to the evolving storyboard
- For example:
  - User story: "As an user I want my information to be available in all of my devices"
  - Architectural story: "Any UI element renders properly in desktop and mobile browsers (e.g., Firefox, Chrome, IE, as well as Apple and Android default mobile browsers)
- The architect works with
  - the product owner to prioritize the architectural stories
  - the team during the sprint to ensure that the evolving software continues to show high architectural quality
- Reviewing working product emerging from the sprint can be a useful form of architectural review

## Further Reading

<span id="page-50-0"></span>

| 202   |
|-------|
|       |
|       |
|       |
|       |
|       |
|       |
|       |
| s 202 |

## *The End*



---

# سند 9: 09_SoftwareTesting

**فایل اصلی:** `09_SoftwareTesting.pdf`

### **Software Testing**

#### **Quality Management: Chapters 22 & 23**

Faezeh Gohari

### Agenda

- Software Testing Concepts
- Unit Testing
- Integration Testing
- System Testing
- Debugging

![](09_SoftwareTesting/09_SoftwareTesting/_page_1_Picture_6.jpeg)

### *Software Testing Concepts*

### Software Testing

**Testing is the process of exercising a program with the specific intent of finding errors prior to delivery to the end user.**

- Testing provides greater assurance that the software is of high **quality** and **reliability**
- Software is **not completed** until it is fully tested from different perspectives
  - Functional characteristics
  - Non-functional characteristics
    - performance, security, usability, …

### What Testing Shows

![](09_SoftwareTesting/09_SoftwareTesting/_page_4_Figure_1.jpeg)

### Costly Software Failures

- Boeing A220: Engines failed after software update allowed excessive vibrations
- Toyota brakes: Dozens dead, thousands of crashes

![](09_SoftwareTesting/09_SoftwareTesting/_page_5_Picture_3.jpeg)

![](09_SoftwareTesting/09_SoftwareTesting/_page_5_Picture_4.jpeg)

- Healthcare website: Crashed repeatedly on launch—never load tested
- Ariane 5 explosion:
   Millions of \$\$

We need our software to be dependable. Testing is one way to assess dependability.

### V & V

- *Verification* refers to the set of tasks that ensure that software correctly implements a specific function.
- *Validation* refers to a different set of tasks that ensure that the software that has been built is traceable to customer requirements. Boehm [Boe81] states this another way:
  - *Verification:* "Are we building the product right?"
  - *Validation:* "Are we building the right product?"

### Who Tests the Software?

![](09_SoftwareTesting/09_SoftwareTesting/_page_7_Picture_1.jpeg)

**Understands the system but, will test "gently" and, is driven by "delivery"**

![](09_SoftwareTesting/09_SoftwareTesting/_page_7_Picture_3.jpeg)

*developer independent tester*

**Must learn about the system, but, will attempt to break it and, is driven by quality**

## Independent Test Group (ITG)

- The software **developer** is **always responsible** for testing the individual **units**
- In many cases, the developer also conducts **integration testing**
- After the software architecture is complete does an **independent test group** become involved
  - To find hidden errors
- The developer and the ITG **work closely** throughout a software project to ensure that thorough tests will be conducted
- While testing is conducted, the developer must be available to correct errors that are uncovered

### Software Testing Dimensions

- Level of testing
  - Unit test, Integration test, System test, Acceptance test
- Method of testing
  - White-box or Black-box
- Type of testing
  - Functional or Non-functional tests
- Execution manner
  - Automated or Manual
- Tester Role
  - Developer, QA, end-user, …

## Testing Levels Based on Software Activities

![](09_SoftwareTesting/09_SoftwareTesting/_page_10_Figure_1.jpeg)

![](09_SoftwareTesting/09_SoftwareTesting/_page_11_Figure_0.jpeg)

### Acceptance Test

- **Acceptance tests** are a series of specific tests **conducted by the customer** in an attempt to uncover product errors before accepting the software from the developer
- When a software product is built for one customer, it is reasonable for that person to conduct a series to validate all requirements
- If software is developed to be used by many customers, it is impractical to allow each user to perform formal acceptance tests
- Most software product builders use a process called **alpha and beta testing** to uncover **errors that only end users seem able to find**

### Alpha and Beta Testing

#### **Alpha testing:**

- Conducted at the **developer's site** by a **representative group of end users**
- The software is used with the **developer** "looking over the shoulder" of the users and **recording errors** and usage problems.
- Alpha tests are conducted in a **controlled environment**

### Alpha and Beta Testing

#### **Beta testing:**

- Conducted at one or more **end-user sites**
- The developer generally is not present
- A "**live**" application of the software in an environment **not controlled by the developer**
- The **customer records all problems** (real or imagined) that are encountered during beta testing and reports these at regular intervals
- The developer makes modifications and then **prepares for release** of the software product to the **entire customer base**

### Colored Boxes

#### **Black-box testing:**

 Derive tests from **external descriptions** of the software, including specifications, requirements, and design

#### **White-box testing:**

- Derive tests from the **source code internals** of the software
  - 1. All independent paths within a module are exercised at least once
  - 2. All logical decisions on their true and false sides
  - 3. All loops at their boundaries and within their bounds
  - 4. All internal data structures to ensure their validity

### *Unit Testing*

## **Unit Testing**

![](09_SoftwareTesting/09_SoftwareTesting/_page_17_Figure_1.jpeg)

### **Unit Testing**

![](09_SoftwareTesting/09_SoftwareTesting/_page_18_Figure_1.jpeg)

### Role of Scaffolding

- Because a unit is not a stand-alone program, some type of scaffolding is required to create a testing framework
  - **Driver** and/or **Stub** software must often be developed for each unit test
- **Driver**: In most applications a driver is nothing more than a "main program" that accepts test-case data, passes such data to the unit (to be tested), and prints relevant results
- **Stubs:** serve to replace units that are subordinate (invoked by) the unit to be tested
  - A stub or "dummy subprogram" uses the subordinate unit's interface, may do minimal data manipulation and returns control to the unit under test

### Unit Test Environment

![](09_SoftwareTesting/09_SoftwareTesting/_page_20_Figure_1.jpeg)

### Scaffolding Overhead

- Drivers and stubs represent testing "overhead"
  - Both are software that must be coded but that is not delivered with the final software product
- If drivers and stubs are kept simple, actual overhead is relatively low
- Unfortunately, many units cannot be adequately tested with "simple" scaffolding software
- In such cases, complete testing can be postponed until the integration test step (where drivers or stubs are also ready to use)

## Control Flow Graph (CFG)

- A **CFG** models all executions of a method by describing control structures
- **Nodes**: Statements or sequences of statements (basic blocks)
- **Edges**: Transfers of control
- **Basic Block**: A sequence of statements such that if the first statement is executed, all statements will be (no branches)
- CFGs are sometimes annotated with extra information
  - branch predicates
  - defs
  - uses

### CFG: The if Statement

```
if (x < y)
{
  y = 0;
  x = x + 1;
}
else
{
  x = y;
}
                               4
                               1
                         2 3
                         x < y x >= y
                 y = 0
               x = x + 1
```

![](09_SoftwareTesting/09_SoftwareTesting/_page_23_Figure_2.jpeg)

x = y

### CFG: The if-Return Statement

```
if (x < y)
{
  return;
}
print (x);
return;
```

![](09_SoftwareTesting/09_SoftwareTesting/_page_24_Picture_2.jpeg)

No edge from node 2 to 3. The return nodes must be distinct.

### CFG: while and for

```
for (x = 0; x < y; x++)
                  {
                    y = f (x, y);
                  }
                  return (x);
                          1
                          x = x + 1
                          2
                     3 5
                   x < y x >= y
        y = f (x, y)
                     4
                  x = 0
  implicitly 
initializes loop
```

![](09_SoftwareTesting/09_SoftwareTesting/_page_25_Figure_2.jpeg)

3 4

x < y x >= y

y =f(x,y)

x = x + 1

implicitly increments loop

### CFG: do Loop

![](09_SoftwareTesting/09_SoftwareTesting/_page_26_Figure_1.jpeg)

### CFG: case (switch) Structure

![](09_SoftwareTesting/09_SoftwareTesting/_page_27_Figure_1.jpeg)

to the next case

```
read ( c) ;
switch ( c )
{
  case 'N':
    z = 25;
  case 'Y':
    x = 50;
    break;
  default:
    x = 0;
    break;
}
print (x);
```

### Mapping Flowchart to CFG

![](09_SoftwareTesting/09_SoftwareTesting/_page_28_Figure_1.jpeg)

Areas bounded by edges and nodes are called *regions* When counting regions, we include the area outside the graph as a region

### Tests on CFG

**Structural Testing (or Control Structure Testing):** Defined on a graph just in terms of nodes and edges

 Basis path testing Loop testing **Our focus in this course**

- …
- **Data Flow Testing:** Requires a graph to be annotated with references to variables
  - Selects test paths of a program according to the locations of definitions and uses of variables in the program

### Independent Path

- Any path through the program that introduces **at least one new** set of statements or a new condition
- For example:
  - A set of independent paths:
    - Path 1: 1-11
    - Path 2: 1-2-3-4-5-10-1-11
    - Path 3: 1-2-3-6-8-9-10-1-11
    - Path 4: 1-2-3-6-7-9-10-1-11
  - So for the above set, the path
    - 1-2-3-4-5-10-1-2-3-6-8-9-10-1-11 is not an independent path
- Paths 1 through 4 constitute **a basis set**

![](09_SoftwareTesting/09_SoftwareTesting/_page_30_Picture_11.jpeg)

### Basis Path Testing

- If you can design tests to force execution of a basis set, then:
  - every statement in the program will have been guaranteed to be executed at least one time
  - and every condition will have been executed on its true and false sides (all branches are tested)
- We **derive test cases** to execute basis paths
- Note: The basis set is **not unique**
  - A number of different basis sets can be derived for a given CFG
- How do you know how many paths to look for?
- The computation of **cyclomatic complexity** provides the answer

## Cyclomatic Complexity

- Cyclomatic complexity is a software metric that provides a quantitative measure of the logical complexity of a program
- In the context of basis path testing, the value of cyclomatic complexity indicates
  - **An upper bound for the number of tests** that must be conducted to ensure that all branches have been executed at least once
- Cyclomatic complexity has a foundation in **graph theory**

#### Computing Cyclomatic Complexity

- Cyclomatic complexity V(G) for a control flow graph G is computed in one of three ways:
- 1. The number of regions of G
- 2. V(G) = E − N + 2 where E is the number of CFG edges and N is the number of CFG nodes
- 3. V(G) = P + 1 where P is the number of predicate nodes contained in the flow graph G

### Cyclomatic Complexity: An Example

- 1. The flow graph has four regions
- *2. V*(*G*) = 11 edges 9 nodes + 2 = 4
- *3. V*(*G*) = 3 predicate nodes + 1 = 4

![](09_SoftwareTesting/09_SoftwareTesting/_page_34_Figure_4.jpeg)

#### Cyclomatic Complexity & Error

**A number of industry studies have indicated that the higher V(G), the higher the probability or errors.**

**modules**

**Basis path testing should be applied to critical modules**

![](09_SoftwareTesting/09_SoftwareTesting/_page_35_Figure_4.jpeg)

**modules in this range are more error prone**

### Loop Testing

- Focuses exclusively on the validity of loop constructs
- Four different classes of loops [Bei90]:
  - 1. simple loops
  - 2. concatenated loops
  - 3. nested loops
  - 4. unstructured loop

# Classes of Loops **Nested Loops Concatenated Loops Unstructured Loops Simple loop**

### Loop Testing: Simple Loops

- The following set of tests can be applied to simple loops:
  - 1. skip the loop entirely
  - 2. only one pass through the loop
  - 3. two passes through the loop
  - 4. m passes through the loop m < n
  - 5. (n-1), n, and (n+1) passes through the loop

where n is the maximum number of allowable passes through the loop.

### Loop Testing: Nested Loops

- If we were to extend the test approach for simple loops to nested loops, the number of possible tests would grow geometrically as the level of nesting increases
- This would result in an impractical number of tests
- Beizer [Bei90] suggests an approach that will help to reduce the number of tests:
  - 1. Start at the **innermost** loop. Set all **other loops to minimum**  values.
  - 2. Conduct **simple loop tests for the innermost** loop while holding the outer loops at their minimum iteration values.
  - **3. Work outward**, conducting tests for the next loop, but keeping all other **outer loops at minimum** values and other **nested loops to "typical"** values.
  - 4. Continue until all loops have been tested.

#### Loop Testing: Concatenated Loops

- If the loops are independent of one another
  - Treat each as a simple loop
- When the loops are not independent
  - The approach applied to nested loops is recommended
  - For example when the final loop counter of loop 1 is used as the initial value of loop 2

#### Unstructured Loops

 Whenever possible, this class of loops should be redesigned to reflect the structured loops

### *Integration Testing*

## Integration Testing Strategies

#### **Options:**

- **• the "big bang" approach**
- **• an incremental construction strategy**

![](09_SoftwareTesting/09_SoftwareTesting/_page_42_Picture_4.jpeg)

### Top Down Integration

![](09_SoftwareTesting/09_SoftwareTesting/_page_43_Figure_1.jpeg)

### Bottom-Up Integration

![](09_SoftwareTesting/09_SoftwareTesting/_page_44_Figure_1.jpeg)

### Sandwich Testing

![](09_SoftwareTesting/09_SoftwareTesting/_page_45_Figure_1.jpeg)

## Continuous Integration

- Merging components into the evolving software increment **once or more each day**
- A common **agile** development practice
- We need quick and efficient integration testing to always have a working program as part of **continuous delivery**
- **Smoke testing** is an integration testing approach that can be used when software is developed by an agile team using short increment build times
  - A continuous integration strategy
  - The software is rebuilt (with new components added) and smoke tested every day
  - Assess the project on a frequent basis

### Smoke Testing-I

- Smoke Test refers to an **initial testing** which is performed on **newly developed software build**
- Determines whether the deployed software **build is stable or not**.
- It acts a confirmation for the team to accept a build or reject and **proceed with further testing**.
- It consists of **a minimal set of tests** that run on each build to test software **core functionalities**.
  - Also called '**Surface Level** Testing '─**not deep**  testing
  - **Low cost** testing
- It is used to ensure that all the critical functionalities are working properly or not.

### Smoke Testing-II

- As it ensures the correctness of the software at the **initial stage**, it requires **less amount of effort and cost**.
- If we don't perform smoke testing at an early stage, **defects may be encountered in later stages** 
  - Costly defects
  - Defects found in the later stage can be **show stopper**
    - May **affect the release** of the deliverables
- Smoke testing minimizes the integration risks

## Smoke Testing Steps

- Software components that have been translated into code are integrated into a "build."
  - A build includes all data files, libraries, reusable modules, and engineered components that are required to implement one or more product functions.
- A series of tests is designed to expose errors that will keep the build from properly performing its function.
  - The intent should be to uncover "show stopper" errors that have the highest likelihood of throwing the software project behind schedule.
- The build is integrated with other builds and the entire product (in its current form) is smoke tested daily.
  - The integration approach may be top down or bottom up.

## Regression Testing

- In **depth** and **through** examination of software to ensure that recent **change** has **not adversely affected** the **existing features**
  - **High cost testing**
- The **re-execution** of some subset of tests that have already been conducted to ensure that changes have not propagated **unintended side effects**
- The verification of software **after any changes**
  - bug fixes, requirement changes, defect fix or any new module development
- In the case of newly developed builds
  - **Smoke** Test is always **followed by Regression** Test
  - Test Cases of Smoke Test is a part of Regression Testing and covers only the core functionalities.
- Regression testing can be done manually or **automated**.

### *System Testing*

## System Testing

- **Recovery testing**
- **Security testing**
- **Stress testing**
- **Performance testing**
- **Deployment testing**

## Recovery Testing

- Many systems must recover from faults and resume processing with little or no downtime.
- A **fault tolerant system**
  - processing faults must not cause overall system function to cease
- Recovery testing is a system test that **forces the software to fail** in a variety of ways and **verifies that recovery is properly performed**.
- If recovery is automatic (performed by the system itself),
  - reinitialization, checkpointing mechanisms, data recovery, and restart are evaluated for correctness.
- If recovery requires human intervention,
  - the mean-time-to-repair (MTTR) is evaluated to determine whether it is within acceptable limits

## Security Testing

- Security testing attempts to **verify** the **protection mechanisms** built into a system to protect it from improper **penetration**.
- Given enough time and resources, good security testing will ultimately penetrate a system.
- The role of the system designer is to make penetration cost more than the value of the information that will be obtained.

### Stress Testing

- Earlier software testing steps result in thorough evaluation of normal program functions and performance
- Stress tests are designed to confront programs with **abnormal situations**
- "How high can we crank this up before it fails?"
- Stress testing executes a system in a manner that demands resources in abnormal quantity or frequency
  - For example, special tests may be designed that generate 10 interrupts per second, when one or two is the average rate
  - test cases that require maximum memory
  - test cases that may cause thrashing in a virtual OS
  - …
- The tester attempts to **break the program**

### Performance Testing

- For **real-time and embedded systems**, software that provides required function but does not conform to performance requirements is unacceptable
- Performance testing is designed to test the **run-time performance** of an integrated software system
- Performance testing occurs **throughout all steps** in the testing process
  - Even at the unit level, the performance of an individual module may be assessed
- However, the **true performance** of a system cannot be assessed until all system elements are **fully integrated**

### Deployment Testing

- In many cases, software must execute on a **variety of platforms** and under more than one operating system environment
- Also called **configuration testing**
- Deployment testing exercises the software in each operating environment
- In addition, deployment testing examines:
  - all installation procedures
  - all specialized installation software (e.g., "installers") that will be used by customers, and
  - all documentation that will be used to introduce the software to end users

### *Debugging*

### Debugging: A Diagnostic Process

- When a test case uncovers an error, debugging is the process that results in the **removal of the error**
- "**Symptomatic**" indication of a problem during test results evaluation
  - The **external manifestation** of the error and its **internal cause** may have **no obvious relationship** to one another
- The process that connects a symptom to a cause is debugging

![](09_SoftwareTesting/09_SoftwareTesting/_page_59_Picture_5.jpeg)

### The Debugging Process

![](09_SoftwareTesting/09_SoftwareTesting/_page_60_Picture_1.jpeg)

### **Debugging Effort**

![](09_SoftwareTesting/09_SoftwareTesting/_page_61_Figure_1.jpeg)

### Symptoms & Causes

![](09_SoftwareTesting/09_SoftwareTesting/_page_62_Figure_1.jpeg)

- **symptom and cause may be geographically remote**
- **symptom may disappear (temporarily) when another error is fixed**
- **symptom may be caused by non-errors (e.g., round-off inaccuracies)**
- **symptom may be caused by human error (not easily traceable)**
- **may be difficult to accurately reproduce input conditions**
- **symptom may be due to causes distributed across multiple tasks running on different processors**

### Further Reading

| 5   |
|-----|
| 523 |
|     |
|     |
|     |
|     |
| 623 |
|     |
|     |

### *The End*



---

# سند 10: 10_Measurement

**فایل اصلی:** `10_Measurement.pdf`

### **Software Measurement: Product, Process and Project Metrics**

**Quality and Project Management: Chapters 30 & 32**

*Slide Set to accompany Software Engineering: A Practitioner's Approach, 8/e* **by Roger S. Pressman and Bruce R. Maxim**

#### *For non-profit educational use only*

May be reproduced ONLY for student use at the university level when used in conjunction with *Software Engineering: A Practitioner's Approach, 8/e.* Any other reproduction or use is prohibited without the express written permission of the author.

## Agenda

- Product Metrics
- Process and Project Metrics
- Software Quality Metrics

![](10_Measurement/10_Measurement/_page_1_Picture_4.jpeg)

### *Product Metrics*

### Product Metrics

- Metrics for the Requirements Model
- Architectural Design Metrics
- Metrics for OO Design
- User Interface Design Metrics
- Metrics for Source Code
- Metrics for Testing
- Metrics for Maintenance

### Metrics for the Requirements Model

- Technical work in software engineering begins with the creation of the requirements model
- Product metrics that provide insight into the quality of the analysis model are desirable
- 1. Function-based metrics
  - The function point metric (FP) is used as a means for **measuring the functionality**  delivered by a system
  - FP measures software size (functional sizing)
- 2. Specification metrics

## Function Point (FP)

- Types of functions in FP
  - Transaction Functions:
  - made up of the processes that are **exchanged** between the user or external applications and the application being measured
    - External Inputs (EI) Input screen and tables
    - External Outputs (EO) Output screen and reports
    - External Inquiries (EQ) Queries and interrupts
  - Data Functions:
  - made up of internal and external **resources** that affect the system
    - Internal Logical Files (ILF) Databases and directories
    - External Interface Files (EIF) Shared databases and routines

### Transactional FP

- External Input (EI):
  - A transaction function in which data goes "into" the application from outside the boundary to inside
    - Data may come from a data input screen or another application
    - Data can be either control or business information
- External Outputs (EO):
  - A transaction function in which data comes "out" of the system
    - Reports or output files sent to other applications
- External Inquiries (EQ):
  - A transaction function with both input and output components that result in data retrieval

### Data FP

- Internal Logical Files (ILF)
  - A group of logically related data or control information that resides entirely within the application boundary
  - The primary intent of an ILF is to hold data required by one or more processes of the application
- External Interface Files (EIF)
  - A group of logically related data or control information that is used by the application
  - The data resides entirely outside the application boundary and is maintained in an ILF by another application
  - An interface has to be developed to get the data from the file

## Computing Function Points-I

| Information                     |       | W      | eighting fac | tor    |            |  |
|---------------------------------|-------|--------|--------------|--------|------------|--|
| Domain Value                    | Count | Simple | Average      | Comple | ×          |  |
| External Inputs (Els)           |       | 3      | 4            | 6      | =          |  |
| External Outputs (EOs)          |       | 4      | 5            | 7      | =          |  |
| External Inquiries (EQs)        |       | 3      | 4            | 6      | =          |  |
| Internal Logical Files (ILFs)   |       | 7      | 10           | 15     | =          |  |
| External Interface Files (EIFs) |       | 5      | 7            | 10     | =          |  |
| Count total                     |       |        |              |        | <b>-</b> [ |  |

- Organizations that use FP methods develop criteria for determining whether a particular entry is simple, average, or complex
- The determination of complexity is somewhat subjective

## Computing Function Points-II

To compute function points (FP):

$$FP = count total \times [0.65 + 0.01 \times \Sigma(F_i)]$$

- count total is the sum of all FP entries
- The Fi (i = 1 to 14) are *value adjustment factors* (VAF) based on responses to 14 questions [Lon02] (see page 660 of 8 th edition)
  - For example: Does the system require reliable backup and recovery?
  - Each question is answered using an ordinal scale that ranges from 0 (not important or applicable) to 5 (absolutely essential(
- Based on the projected FP value derived from the requirements model, the project team can estimate the overall implementation size of the system
  - Assume that past projects have found that one FP translates into 60 lines of code (with an object-oriented language)
  - These historical data provide the project manager with important planning information that is based on the requirements model rather than preliminary estimates

## An Example of Computing FP-I

![](10_Measurement/10_Measurement/_page_10_Figure_1.jpeg)

- Consider the flow diagram for a **user interaction function** within SafeHome software
- The function manages user interaction, accepting a user password to activate or deactivate the system, and allows inquiries on the status of zones and sensors
- The function displays a series of prompting messages and sends appropriate control signals to various components of the security system

# An Example of Computing FP-II

| Information                     |       | W        | eighting fac | tor     |
|---------------------------------|-------|----------|--------------|---------|
| Domain Value                    | Count | Simple   | Average      | Complex |
| External Inputs (Els)           | 3     | 3        | 4            | 6 = 9   |
| External Outputs (EOs)          | 2     | 4        | 5            | 7 = 8   |
| External Inquiries (EQs)        | 2     | 3        | 4            | 6 = 6   |
| Internal Logical Files (ILFs)   | 1     | 7        | 10           | 15 = 7  |
| External Interface Files (EIFs) | 4     | <b>5</b> | 7            | 10 = 20 |
| Count total                     |       |          |              | 50      |

- For the purposes of this example, we assume that ∑(Fi) is 46 (a moderately complex product)
- Therefore:

$$FP = 50 \times [0.65 + (0.01 \times 46)] = 56$$

### Specification-Based Metrics

- Davis proposes a list of characteristics to assess the quality of the requirements specification [Dav93]:
  - Specificity (lack of ambiguity)
  - Completeness
  - Correctness
  - Understandability
  - Verifiability
  - Consistency
  - Achievability
  - Concision
  - Traceability
  - Modifiability
  - Precision
  - Reusability

### Specificity

- Assume that there are n<sup>r</sup> requirements in a specification
- To determine the specificity of requirements, Davis suggests a metric that is based on the consistency of the reviewers' interpretation of each requirement:

$$Q_{_1} = \frac{n_{_{ui}}}{n_{_r}}$$

- where nui is the number of requirements for which all reviewers had identical interpretations
- The closer the value of Q to 1, the lower is the ambiguity of the specification

## Architectural Design Metrics

- Architectural design complexity metrics
  - Structural complexity = g(fan-out)
  - Data complexity = f(input & output variables, fan-out)
  - System complexity = h(structural & data complexity)
- Morphology (i.e., shape) metrics: a function of the number of modules and the number of interfaces between modules

## Structural Complexity

 For hierarchical architectures (e.g., call-andreturn architectures), structural complexity of a module *i* is defined as:

$$S(i) = f_{\text{out}}^2(i)$$

where *fout(i)* is the fan-out of module *i*

### Data Complexity

 Provides an indication of the complexity in the internal interface for a module *i* and is defined as:

$$D(i) = \frac{v(i)}{[f_{\text{out}}(i) + 1]}$$

 where *v*(*i*) is the number of input and output variables that are passed to and from module *i*

## System Complexity

 The sum of structural and data complexity, specified as:

$$C(i) = S(i) + D(i)$$

- As each of these complexity values increases, the overall architectural complexity of the system also increases
- This leads to a greater likelihood that integration and testing effort will also increase

# Morphology Metrics

![](10_Measurement/10_Measurement/_page_18_Picture_1.jpeg)

Referring to the call-and-return architecture:

Size = 
$$n + a$$

- n is the number of nodes and a is the number of arcs
- In this example:
  - Size = 17 + 18 = 35
- Depth = longest path from the root (top) node to a leaf
  - For the above architecture, depth = 4
- Width = maximum number of nodes at any one level of the architecture
  - For the above architecture, width = 6
- The arc-to-node ratio, r = a/n, measures the connectivity density of the architecture and may provide a simple indication of the coupling of the architecture.

## Metrics for OO Design-I

- Whitmire [Whi97] describes nine distinct and measurable characteristics of an OO design:
  - Size
    - A static count of OO entities such as classes or operations, coupled with the depth of an inheritance tree
  - Complexity
    - How classes of an OO design are interrelated to one another
  - Coupling
    - Counting the physical connections between elements of the OO design
    - e.g., the number of messages passed between objects
  - Sufficiency
    - "the degree to which an abstraction [class] possesses the features required of it…"
  - Completeness
    - Whether a class delivers the set of properties that fully reflect the needs of the problem domain

### Metrics for OO Design-II

#### Cohesion

• The degree to which all operations working together to achieve a single, well-defined purpose

#### Primitiveness

• The degree to which an operation is atomic

#### Similarity

• The degree to which two or more classes are similar in terms of their structure, function, behavior, or purpose

#### Volatility

• Measures the likelihood that a change will occur

### Class-Oriented Metrics

- The **CK** metrics suite
  - The most widely referenced sets of OO metrics
  - proposed by **C**hidamber and **K**emerer [Chi94]:
  - 1. weighted methods per class
  - 2. depth of the inheritance tree
  - 3. number of children
  - 4. coupling between object classes
  - 5. response for a class
  - 6. lack of cohesion in methods

### Weighted Methods per Class (WMC)

- Assume that n methods of complexity c1, c2, …, cn are defined for a class C
- The specific complexity metric that is chosen (e.g., cyclomatic complexity) should be normalized so that nominal complexity for a method takes on a value of 1.0

$$WMC = \sum c_i$$

- The number of methods and their complexity indicates the amount of effort required to implement and test a class
- The larger the number of methods, the more complex is the inheritance tree
- As the number of methods grows for a given class, it is likely to become more and more application specific, thereby limiting potential reuse
- For all of these reasons, WMC should be kept as low as possible

### Depth of the Inheritance Tree (DIT)

- The maximum length from the leaf node to the root of the tree
- As DIT grows, it is likely that lower-level classes will inherit many methods
  - Leading to potential difficulties when attempting to predict the behavior of a class
- A deep class hierarchy (DIT is large) also leads to greater design complexity
- On the positive side, large DIT values imply that many methods may be reused

### Number Of Children (NOC)

- The subclasses that are immediately subordinate to a class in the class hierarchy
- As NOC increases,
  - the abstraction represented by the parent class can be diluted if some of the children are not appropriate members of the parent class
  - the amount of testing also increases (required to exercise each child in its operational context)

#### Coupling Between Object classes (CBO)

- The number of collaborations listed for a class on its CRC index card
- As CBO increases,
  - it is likely that the reusability of a class will decrease
  - modifications and testing are also complicated
- CBO for each class should be kept as low as is reasonable

### Response For a Class (RFC)

- The response set of a class:
  - "a set of methods that are executed in response to a message received by an object of that class"
- RFC is the number of methods in the response set
- As RFC increases, the effort required for testing also increases
  - because the test sequence grows
- As RFC increases, the overall design complexity of the class increases

### Lack of Cohesion in Methods (LCOM)

- Each method within a class accesses one or more attributes
- LCOM: The number of methods that access one or more of the same attributes
- If no methods access the same attributes LCOM = 0
- Consider a class with six methods. Four of the methods have one or more attributes in common (i.e., they access common attributes) LCOM = 4
- If LCOM is high, methods may be coupled to one another via attributes
  - This increases the complexity of the class design
- Although there are cases in which a high LCOM is justifiable, it is desirable to keep LCOM low

## User Interface Design Metrics

- Significant literature on the design of UI
- But little information on quality metrics
- In the following, we present some design metrics that may have application for:
  - websites, browser-based applications, and mobile applications
  - Many of these metrics are applicable to all user interfaces
- UI design metrics:
  - 1. Interface Metrics
  - 2. Aesthetic (Graphic Design) Metrics
  - 3. Content Metrics
  - 4. Navigation Metrics

### Interface Metrics

#### Suggested Metric

Layout appropriateness

Layout complexity

Layout region complexity

Recognition complexity

Recognition time

Typing effort

Mouse pick effort

Selection complexity

Content acquisition time

Memory load

#### Description

The relative position of entities within the interface

Number of distinct regions defined for an interface

Average number of distinct links per region

Average number of distinct items the user must look at before

making a navigation or data input decision

Average time (in seconds) that it takes a user to select the

appropriate action for a given task

Average number of keystrokes required for a specific function

Average number of mouse picks per function

Average number of links that can be selected per page

Average number of words of text per Web page

Average number of distinct data items that the user must

remember to achieve a specific objective

### Aesthetic (Graphic Design) Metrics

| Suggested Metric                | Description                                                                                  |
|---------------------------------|----------------------------------------------------------------------------------------------|
| Word count                      | Total number of words that appear on a page                                                  |
| Body text percentage            | Percentage of words that are body versus display text (e.g., headers)                        |
| Emphasized body text percentage | Portion of body text that is emphasized (e.g., bold, capitalized)                            |
| Text positioning count          | Changes in text position from flush left                                                     |
| Text cluster count              | Text areas highlighted with color, bordered regions, rules, or lists                         |
| Link count                      | Total links on a page                                                                        |
| Page size                       | Total bytes for the page as well as elements, graphics, and style sheets                     |
| Graphic percentage              | Percentage of page bytes that are for graphics                                               |
| Graphics count                  | Total graphics on a page (not including graphics specified in scripts, applets, and objects) |
| Color count                     | Total colors employed                                                                        |
| Font count                      | Total fonts employed (i.e., face + size + bold + italic)                                     |

### Content Metrics

| Suggested Metric         | Description                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| Page wait                | Average time required for a page to download at different connection speeds |
| Page complexity          | Average number of different types of media used on page, not including text |
| Graphic complexity       | Average number of graphics media per page                                   |
| Audio complexity         | Average number of audio media per page                                      |
| Video complexity         | Average number of video media per page                                      |
| Animation complexity     | Average number of animations per page                                       |
| Scanned image complexity | Average number of scanned images per page                                   |
|                          |                                                                             |

### Navigation Metrics

| Suggested Metric        | Description                                                               |
|-------------------------|---------------------------------------------------------------------------|
| Page-linking complexity | Number of links per page                                                  |
| Connectivity            | Total number of internal links, not including dynamically generated links |
| Connectivity density    | Connectivity divided by page count                                        |

### Metrics for Source Code

- Halstead's Software Science: a comprehensive collection of metrics all predicated on the number (count and occurrence) of operators and operands within a program
- n1 = number of distinct operators in a program
- n2 = number of distinct operands in a program
- N1 = total number of operator occurrences
- N2 = total number of operand occurrences
- The overall program length:

$$N = n1 \log_2 n1 + n2 \log_2 n2$$

The program volume:

$$V = N \log_2 (n1 + n2)$$

- V will vary with programming language and represents the volume of information (in bits) required to specify a program
- Lower volume is more desirable

## Metrics for Testing-I

- Testing metrics
  - 1. Metrics that attempt to predict the likely number of tests required at various testing levels
  - 2. Metrics that focus on test coverage for a given component
- Architectural design metrics provide information on
  - the ease or difficulty of testing
  - and the need for specialized testing software (e.g., stubs and drivers)
- Cyclomatic complexity (a component-level design metric) lies at the core of basis path testing
  - Modules with high cyclomatic are more likely to be error prone than modules whose cyclomatic complexity is lower
  - Cyclomatic complexity can be used to target modules as candidates for extensive unit testing

## Metrics for Testing-II

- Testing effort can also be estimated using metrics derived from Halstead measures
  - See page 676 of 8 th edition
- Binder [Bin94] suggests a broad array of design metrics that have a direct influence on the "testability" of an OO system.
  - Lack of cohesion in methods (LCOM).
  - Percent public and protected (PAP).
  - Public access to data members (PAD).
  - Number of root classes (NOR).
  - Fan-in (FIN).
  - Number of children (NOC) and depth of the inheritance tree (DIT).

### Metrics for Maintenance

- IEEE Std. 982.1-1988 [IEE94] suggests a *software maturity index* (SMI) that provides an indication of the stability of a software product (based on changes that occur for each release of the product). The following information is determined:
  - *M<sup>T</sup>* = the number of modules in the current release
  - *F<sup>c</sup>* = the number of modules in the current release that have been changed
  - *F<sup>a</sup>* = the number of modules in the current release that have been added
  - *F<sup>d</sup>* = the number of modules from the preceding release that were deleted in the current release
- The software maturity index is computed in the following manner:
  - SMI = [*M<sup>T</sup>* - (*F<sup>a</sup>* + *F<sup>c</sup>* + *F<sup>d</sup>* )]/*M<sup>T</sup>*
- As SMI approaches 1.0, the product begins to stabilize.

### *Process and Project Metrics*

## A Good Manager Measures

![](10_Measurement/10_Measurement/_page_38_Figure_1.jpeg)

These slides are designed to accompany *Software Engineering: A Practitioner's Approach, 8/e*  (McGraw-Hill 2014). Slides copyright 2014 by Roger Pressman.

### Why Do We Measure?

- **Process metrics** are collected across all projects and over long periods of time
  - Their intent is to provide a set of process indicators that lead to long-term software process improvement
- **Project metrics** enable a software project manager to:
  - assess the status of an ongoing project
  - track potential risks
  - uncover problem areas before they go "critical"
  - adjust work flow or tasks
  - evaluate the project team's ability to control quality of software work products

### Process Measurement

- We measure the efficacy of a software process indirectly.
  - That is, we derive a set of metrics based on the outcomes that can be derived from the process.
  - Outcomes include
    - measures of errors uncovered before release of the software
    - defects delivered to and reported by end-users
    - work products delivered (productivity)
    - human effort expended
    - calendar time expended
    - schedule conformance
    - other measures.
- We also derive process metrics by measuring the characteristics of specific software engineering tasks.
  - For example, the effort and time spent performing the umbrella activities and framework activities

### Statistical Software Process Improvement

- A more rigorous approach called statistical software process improvement (SSPI)
  - As an organization becomes more comfortable with the **collection and use** of process metrics

![](10_Measurement/10_Measurement/_page_41_Figure_3.jpeg)

### Project Metrics

#### Intent

- To minimize the development schedule by making the adjustments necessary to avoid delays and mitigate potential problems and risks
- To assess product quality on an ongoing basis and, when necessary, modify the technical approach to improve quality
- Typical Project Metrics
  - Effort/time per software engineering task
  - Errors uncovered per review hour
  - Scheduled vs. actual milestone dates
  - Changes (number) and their characteristics
  - Distribution of effort on software engineering tasks

## Comparing Projects

- But how does an organization compare metrics that come from different individuals or projects?
- Consider a simple example:
  - Team A found 342 errors during the software process prior to release
  - Team B found 184 errors
  - Which team is more effective in uncovering errors throughout the process?
    - Because you do not know the size or complexity of the projects, you cannot answer this question
- If the measures are normalized, it is possible to create software metrics that enable comparison to broader organizational averages

### Size-Oriented Metrics

- Size-oriented software metrics are derived by normalizing quality and/or productivity measures by considering the size of the software
  - E.g., lines of code (LOC), person-months effort, cost, number of pages of documentation, …

| Project                | LOC                        | Effort         | \$(000)           | Pp. doc.            | Errors            | Defects        | People      |
|------------------------|----------------------------|----------------|-------------------|---------------------|-------------------|----------------|-------------|
| alpha<br>beta<br>gamma | 12,100<br>27,200<br>20,200 | 24<br>62<br>43 | 168<br>440<br>314 | 365<br>1224<br>1050 | 134<br>321<br>256 | 29<br>86<br>64 | 3<br>5<br>6 |
|                        |                            |                |                   |                     |                   |                |             |

## Typical Size-Oriented Metrics

- Choosing lines of code (LOC) as a normalization value
  - errors per KLOC (thousand lines of code)
  - defects per KLOC
  - \$ per LOC
  - pages of documentation per KLOC
- Choosing effort as a normalization value
  - errors per person-month
  - LOC per person-month
- Other interesting metrics
  - errors per review hour
  - \$ per page of documentation

### Function-Oriented Metrics

- Function-oriented software metrics use a measure of the functionality delivered by the application as a normalization value
- The most widely used function-oriented metric is the function point (FP)
- Proponents
  - programming language–independent
  - Based on data that are more likely to be known early in the evolution of a project
    - Making FP more attractive as an estimation approach
- Opponents
  - Requires some "sleight of hand" in that computation is based on subjective rather than objective data
  - No direct physical meaning—it's just a number

## Typical Function-Oriented Metrics

- errors per FP
- defects per FP
- \$ per FP
- pages of documentation per FP
- FP per person-month

### *Software Quality Metrics*

## Measuring Quality

- Correctness the degree to which a program operates according to specification
- Maintainability—the degree to which a program is amenable to change
- Integrity—the degree to which a program is impervious to outside attack
- Usability—the degree to which a program is easy to use

### Correctness

- Defects (lack of correctness) are those problems reported by a user of the program after the program has been released
- Defects are counted over a standard period of time, typically one year
- The most common measure for correctness:
  - **Defects per KLOC**

### Maintainability

- The ease with which a program can be
  - corrected if an error is encountered,
  - adapted if its environment changes, or
  - enhanced if the customer desires a change in requirements
- There is no way to measure maintainability directly
  - We must use indirect measures
- A simple time-oriented metric is **mean time to change (MTTC)**
  - The time it takes to analyze the change request, design an appropriate modification, implement the change, test it, and distribute the change to all user

## Integrity

- A system's ability to withstand attacks to its security
  - Both accidental and intentional attacks
- To measure integrity, two additional attributes must be defined:
  - **Threat:** The probability that an attack of a specific type will occur within a given time
    - Can be estimated or derived from empirical evidence
  - **Security:** The probability that the attack of a specific type will be repelled
    - Can be estimated or derived from empirical evidence
- The integrity of a system:

Integrity = 
$$\Sigma[1 - (\text{threat} \times (1 - \text{security}))]$$

### Integrity: An Example

- If
  - threat (the probability that an attack will occur) is 0.25
  - security (the likelihood of repelling an attack) is 0.95
- Then
  - the integrity of the system is 0.99 **(very high)**
- If, on the other hand,
  - the threat probability is 0.50
  - the likelihood of repelling an attack is only 0.25,
  - the integrity of the system is 0.63 **(unacceptably low)**

## Usability

- Usability is an attempt to quantify ease of use
- It can be measured in terms of the usability characteristics:
  - Is the system usable without continual help?
  - Does the user know where she is at all times?
  - Are interaction mechanisms, icons, and procedures consistent across the interface?
  - Does the interaction anticipate errors and help the user correct them?
  - Is the interaction simple?
  - ...
- (see Chapter 15 for details)

### Defect Removal Efficiency

 DRE: A quality metric that provides benefit at both the project and process level

$$\mathsf{DRE} = E / (E + D)$$

#### *where:*

*E* is the number of errors found before delivery of the software to the end-user *D* is the number of defects found after delivery

### DRE Advice

- The ideal value for DRE is 1
  - That is, no defects are found in the software
- As E increases (for a given value of D), the overall value of DRE begins to approach 1
- If DRE is low as you move through analysis and design, spend some time improving the way you conduct formal technical reviews
  - For finding as many errors as possible before delivery

### Task-Specific DRE

- DRE can be used within the project to assess a team's ability to find errors before they are passed to the next framework activity or software engineering task
- For example, requirements analysis produces a requirements model
  - It can be reviewed to find and correct errors
  - Those errors that are not found during the review of the requirements model are passed on to design (where they may or may not be found)

$$\mathrm{DRE}_i = \frac{E_i}{E_i + E_{i+1}}$$

*Ei : number of errors found during action i Ei+1 : number of errors found during action i+1 (not discovered in action i)*

## Further Reading

| PART THREE | QUALITY MA | NAGEMENT 411                             |
|------------|------------|------------------------------------------|
|            | CHAPTER 19 | Quality Concepts 412                     |
|            | CHAPTER 20 | Review Techniques 431                    |
|            | CHAPTER 21 | Software Quality Assurance 448           |
|            | CHAPTER 22 | Software Testing Strategies 466          |
|            | CHAPTER 23 | Testing Conventional Applications 496    |
|            | CHAPTER 24 | Testing Object-Oriented Applications 523 |
|            | CHAPTER 25 | Testing Web Applications 540             |
|            | CHAPTER 26 | Testing MobileApps 567                   |
|            | CHAPTER 27 | Security Engineering 584                 |
|            | CHAPTER 28 | Formal Modeling and Verification 601     |
|            | CHAPTER 29 | Software Configuration Management 623    |
|            | CHAPTER 30 | Product Metrics 653                      |
| PART FOUR  | MANAGING   | SOFTWARE PROJECTS 683                    |
|            | CHAPTER 31 | Project Management Concepts 684          |
|            | CHAPTER 32 | Process and Project Metrics 703          |
|            | CHAPTER 33 | Estimation for Software Projects 727     |
|            | CHAPTER 34 | Project Scheduling 754                   |
|            | CHAPTER 35 | Risk Management 777                      |
|            | CHAPTER 36 | Maintenance and Reengineering 795        |
|            |            |                                          |

### *The End*



---

# سند 11: 11_Reengineering

**فایل اصلی:** `11_Reengineering.pdf`

## **Maintenance & Reengineering**

#### **Chapter 36**

*Slide Set to accompany Software Engineering: A Practitioner's Approach, 7/e* **by Roger S. Pressman**

**Slides copyright © 1996, 2001, 2005, 2009 by Roger S. Pressman**

#### *For non-profit educational use only*

May be reproduced ONLY for student use at the university level when used in conjunction with *Software Engineering: A Practitioner's Approach, 7/e.* Any other reproduction or use is prohibited without the express written permission of the author.

All copyright information MUST appear if these slides are posted on a website for student use.

## Agenda

- Software Maintenance
- Business Process Reengineering
- Software Reengineering
- Economics of Reengineering

![](11_Reengineering/11_Reengineering/_page_1_Picture_5.jpeg)

### Software Maintenance

- Software is released to end-users, and
  - within days, bug reports filter back to the software engineering organization.
  - within weeks, one class of users indicates that the software must be changed so that it can accommodate the special needs of their environment.
  - within months, another corporate group who wanted nothing to do with the software when it was released, now recognizes that it may provide them with unexpected benefit. They'll need a few enhancements to make it work in their world.
- All of this work is *software maintenance*

### Maintainable Software

- Maintainable software exhibits effective modularity
- It makes use of design patterns that allow ease of understanding.
- It has been constructed using well-defined coding standards and conventions, leading to source code that is self-documenting and understandable.
- It has undergone a variety of quality assurance techniques that have uncovered potential maintenance problems before the software is released.
- It has been created by software engineers who recognize that they may not be around when changes must be made.
  - *Therefore, the design and implementation of the software must "assist" the person who is making the change*

## Reengineering-I

- Instead of embedding outdated processes in software, we should obliterate them and start over
- We should "reengineer" our businesses:
  - use the power of modern information technology to radically redesign our business processes in order to achieve dramatic improvements in their performance

![](11_Reengineering/11_Reengineering/_page_4_Figure_4.jpeg)

## Reengineering-II

- The nexus between business reengineering and software engineering lies in a "**system view**"
- As managers work to modify business rules to achieve greater effectiveness and competitiveness, software must keep pace
- In some cases, this means the creation of major new computer-based systems
- But in many others, it means the modification or rebuilding of existing applications

#### Business Process-I

- A set of logically related tasks performed to achieve a defined business outcome
- Within the business process, people, equipment, material resources are combined to produce a specified result
- Examples of business processes include designing a new product, purchasing services and supplies, hiring a new employee, and paying suppliers
  - Each demands a set of tasks and diverse resources within the business
- Every business process has a defined customer—a person or group that receives the outcome (e.g., an idea, a report, a design, a service, a product)

#### Business Process-II

- Business processes cross organizational boundaries
  - They require different organizational groups participate in the "logically related tasks" that define the process
- Every system is actually a hierarchy of subsystems.
  - A business is no exception
  - The business business systems business processes business subprocesses
  - **business system** (also called **business function**)

# Business Process Reengineering (BPR)

- **BPR:** The search for, and the implementation of, radical change in business process to achieve breakthrough results
- Business hierarchy:
  - The business business systems business processes business subprocesses
- BPR can be applied at any level of the hierarchy
- But as the scope of BPR broadens (i.e., as we move upward in the hierarchy), the risks associated with BPR grow dramatically
- For this reason, most BPR efforts focus on individual processes or subprocesses

### A BPR Model

11 Like most engineering activities, business process reengineering is iterative Business goals and the processes that achieve them must be adapted to a changing business environment

#### A BPR Model

- **Business definition.** Business goals are identified within the context of **four key drivers**: cost reduction, time reduction, quality improvement, and personnel development and empowerment.
- **Process identification.** Processes that are **critical to achieving the goals** defined in the business definition are identified.
- **Process evaluation.** The existing process is thoroughly **analyzed and measured**.
- **Process specification and design.** Based on information obtained during the first three BPR activities, **use-cases are prepared** for each process that is to be redesigned.
- **Prototyping.** A redesigned business process must be prototyped to **get feedback** before it is fully integrated into the business.
- **Refinement and instantiation.** Based on feedback from the prototype, the business process is **refined and then instantiated**  within a business system.

#### Software Reengineering-I

- The scenario is all too common:
  - An application has served the business needs of a company for 10 or 15 years
  - During that time it has been corrected, adapted, and enhanced many times
  - Now the application is unstable
    - It still works, but every time a change is attempted, unexpected and serious side effects occur
  - Yet the application must continue to evolve
  - What to do?
- Solution: software reengineering
- Unmaintainable software is not a new problem
  - software reengineering has been spawned by software maintenance problems

#### Software Reengineering-II

- Reengineering takes time, it costs significant amounts of money
  - So it is not accomplished in a few months or even a few years
- Reengineering of information systems is an activity that will absorb information technology resources for many years
- That's why every organization needs a pragmatic strategy for software reengineering
  - We need a reengineering process model

#### Reengineering: An analogous Example

- Reengineering is a rebuilding activity
- To better understand it, consider:
  - An analogous activity: the rebuilding of a house
  - How would you proceed?
- 1. Before you can start rebuilding, it would seem reasonable to inspect the house based on a list of criteria
- 2. Before you tear down and rebuild the entire house, be sure that the structure is weak
  - If the house is structurally sound, it may be possible to "remodel" without rebuilding (at much lower cost and in much less time)

#### Reengineering: An analogous Example

- 3. Before you start rebuilding be sure you understand how the original was built
  - Understand the wiring, the plumbing,...
  - Even if you trash them all, the insight you'll gain will serve you for the new construction
- 4. If you begin to rebuild, use only the most modern, long-lasting materials
  - This may cost a bit more now, but it will help you to avoid expensive and time-consuming maintenance later
- 5. If you decide to rebuild, be disciplined about it
  - Use practices that will result in high quality—today and in the future
- These principles apply equally well to the reengineering of computer-based systems

# A Software Reengineering Process Model

![](11_Reengineering/11_Reengineering/_page_15_Picture_1.jpeg)

# A Software Reengineering Process Model

- It is a cyclical model
  - Each of the activities may be repeated
- In some cases, these activities occur in a linear sequence, but this is not always the case
  - For example, it may be that reverse engineering (understanding the internal workings of a program) may have to occur before document restructuring can commence
- The process can terminate after any one of these activities

![](11_Reengineering/11_Reengineering/_page_16_Picture_6.jpeg)

## Inventory Analysis-I

- Every software organization should have an inventory of all applications
- The inventory can be nothing more than a spreadsheet model
  - provides a detailed description (e.g., size, age, business criticality) of every active application
- For example, the inventory may be a table that contains a list of criteria, e.g.,
  - name of the application
  - year it was originally created
  - number of substantive changes made to it
  - total effort applied to make these changes
  - date of last substantive change
  - effort applied to make the last change
  - applications to which it interfaces, ...

## Inventory Analysis-II

- Applications are sorted according to
  - business criticality, longevity, current maintainability and supportability, and other locally important criteria
- By sorting this information, candidates for reengineering appear
- Resources can then be allocated to candidate applications for reengineering work
- The inventory should be revisited on a regular basis
  - The status of applications (e.g., business criticality) can change as a function of time
  - As a result, priorities for reengineering will shift

## Document Restructuring

- Weak documentation is the trademark of many legacy systems
- But what can we do about it? What are our options?
- Options …
  - *Creating documentation is far too time consuming.* In some cases, creating documentation when none exists is simply too costly.
    - If the system works, we'll live with what we have. In some cases, this is the correct approach.
  - *Documentation must be updated, but we have limited resources.* In other cases, some documentation must be created, but only when changes are made.
    - We'll use a "document when touched" approach. It may not be necessary to fully re-document an application.
    - If a modification occurs, document it.
  - *The system is business critical and must be fully re-documented.*  Even in this case, an intelligent approach is to keep documentation to an essential minimum.

#### Reverse Engineering

- What is Reverse engineering?
- Reverse engineering for software is the process of analyzing a program
  - to create a representation of the program at a higher level of abstraction than source code
- Reverse engineering is a process of design recovery
- Reverse engineering tools extract database design, architectural design, and procedural design information from an existing program

## Code Restructuring

- One of the most important part of reengineering is code restructuring
- In some legacy systems, individual modules were coded in a way that makes them difficult to understand, test, and maintain
- In such cases, the code within the suspect modules can be restructured

## Code Restructuring Steps

- Source code is analyzed using a restructuring tool
- Poorly design code segments are redesigned
- Violations of structured programming constructs are noted and code is then restructured (this can be done automatically)
- Code may be rewritten in a more modern programming language
- The new restructured code is reviewed and tested to ensure that no anomalies have been introduced
- Internal code documentation is updated

## Data Restructuring

- A program with weak data architecture will be difficult to adapt and enhance
- In fact, for many applications, information architecture has more influence on the longterm viability of a program than the source code itself
- Because data architecture has a strong influence on program architecture and the algorithms that populate it,
  - changes to the data architecture will invariably result in either architectural or code-level changes

## Data Restructuring Steps

- In most cases, data restructuring begins with a reverse engineering activity
- Current data architecture is extracted and necessary data models are defined
- Data objects and attributes are identified, and existing data structures are reviewed for quality
- When data structure is weak, the data are reengineered
  - e.g., flat files are currently implemented, whereas a relational approach would greatly simplify processing

## Forward Engineering

- New requirements and the direction of change are identified
- Redesign of the software architecture (program and/or data structure), using modern design concepts
- A complete software configuration (documents, programs and data) will be developed
- CASE tools will automate some parts of the job

## The reverse engineering process

![](11_Reengineering/11_Reengineering/_page_26_Figure_1.jpeg)

# The reverse engineering process

- Before reverse engineering activities can commence, unstructured ("dirty") source code is restructured
  - so that it contains only the structured programming constructs
  - This makes the source code **easier to read** and provides the basis for all the subsequent reverse engineering activities

![](11_Reengineering/11_Reengineering/_page_27_Picture_4.jpeg)

# The reverse engineering process

- The core of reverse engineering is an activity called extract abstractions
- Evaluate the old program and from the source code, develop a meaningful specification of:
  - the processing that is performed,
  - the user interface that is applied,
  - and the program data structures or database that is used

![](11_Reengineering/11_Reengineering/_page_28_Picture_6.jpeg)

#### Reverse Engineering to Understand Data

- It is often the first reengineering task
- Reverse engineering of data occurs at different levels of abstraction
- At the program level, internal program data structures must often be reverse engineered
- At the system level, global data structures (e.g., files, databases) are often reengineered to accommodate new database management paradigms
  - e.g., the move from flat file to relational or objectoriented database systems

#### Reverse Engineering to Understand Data (cont.)

#### Internal data structures

- Reverse engineering techniques for internal program data focus on the definition of classes
- Examining the program code with the intent of grouping related program variables
- For example, record structures, files, lists, and other data structures often provide an initial indicator of classes

#### Reverse Engineering to Understand Data (cont.)

#### Database structure

- Reengineering one database schema into another requires an understanding of existing objects and their relationships
- The following steps may be used to define the existing object model as a precursor to reengineering a new database model:
  - 1. Build an initial object model
  - 2. Determine candidate keys (the attributes are examined to determine whether they are used to point to another record or table)
  - 3. Refine the initial classes
  - 4. Define generalizations
  - 5. Discover associations

#### Reverse Engineering to Understand Processing

- To understand procedural abstractions, the code is analyzed at varying levels of abstraction:
  - system, program, component, pattern, and statement
- Each of the programs that make up the system represents a functional abstraction at a high level of detail
  - A block diagram, representing the interaction between these functional abstractions, is created
- Each component performs some subfunction and represents a defined procedural abstraction
  - A processing narrative for each component is developed
- In some situations, system, program, and component specifications already exist
  - When this is the case, the specifications are reviewed for conformance to existing code

#### Reverse Engineering User Interface

- To fully understand an existing user interface, the structure and behavior of the interface must be specified
- Three basic questions that must be answered as reverse engineering of the UI commences:
  - 1. What are the basic actions (e.g., keystrokes and mouse clicks) that the interface must process?
  - 2. What is the behavioral response of the system to these actions?
  - 3. What concept of existing interface is relevant and what should be replaced?

#### Reverse Engineering User Interface (cont.)

- Behavioral modeling notation (Chapter 11) can provide a means for developing answers to the first two questions
- It is important to note that a replacement GUI may be radically different from the old interface
- It is often worthwhile to develop a new interaction metaphor
  - For example, an old UI requests that a user provide a scale factor (ranging from 1 to 10) to shrink or magnify a graphical image
  - A reengineered GUI might use a touch-screen slide bar to accomplish the same function

# Economics of Reengineering-I

- In a perfect world, every unmaintainable program would be retired immediately,
  - to be replaced by high-quality, reengineered applications developed using modern software engineering practices
- But we live in a world of limited resources
- Reengineering drains resources that can be used for other business purposes
- Therefore, before an organization attempts to reengineer an existing application, it should perform a cost-benefit analysis

# Economics of Reengineering-II

- A cost/benefit analysis model for reengineering has been proposed by Sneed [Sne95]. Nine parameters are defined:
  - P1= current annual maintenance cost for an application.
  - P<sup>2</sup> = current annual operation cost for an application.
  - P3= current annual business value of an application.
  - P<sup>4</sup> = predicted annual maintenance cost after reengineering.
  - P<sup>5</sup> = predicted annual operations cost after reengineering.
  - P<sup>6</sup> = predicted annual business value after reengineering.
  - P<sup>7</sup> = estimated reengineering costs.
  - P<sup>8</sup> = estimated reengineering calendar time.
  - P<sup>9</sup> = reengineering risk factor.
  - L = expected life of the system.

## **Economics of Reengineering-III**

■ The cost associated with continuing maintenance of a candidate application (i.e., reengineering is not performed) can be defined as:

$$C_{\text{maint}} = [P_3 - (P_1 + P_2)] \times L$$

■ The cost associated with reengineering are defined using the following relationship:

$$C_{\text{reeng}} = [P_6 - (P_4 + P_5)] \times (L - P_8) - (P_7 \times P_9)$$

Using the costs presented in equations above, the overall benefit of reengineering can be computed as:

$$cost benefit = C_{reeng} - C_{maint}$$

- The cost-benefit analysis can be performed for all high-priority applications identified during inventory analysis
- Those applications that show the highest cost-benefit can be targeted for reengineering, while work on others can be postponed until resources are available

![](11_Reengineering/11_Reengineering/_page_38_Picture_0.jpeg)
