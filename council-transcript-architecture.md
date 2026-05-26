# LLM Council Transcript
**Date:** 2026-05-21
**Topic:** Optimal architecture for managing 70+ skills (Global vs Local)

## The Framed Question
The user has a Gemini/Claude AI agent setup with a global `user_rules.md` file that currently injects routing instructions and descriptions for 70+ diverse skills (including heavy bioinformatics plugins and marketing tools) into every single prompt, regardless of the active project. This exhausts their context window limits immediately, leading to failures.
The proposed solution is to move from a 'global monolithic skill loading' approach to a 'project-specific plugin architecture'. This involves:
1. Deleting manual skill routing rules ("If task is X, use skill Y") and trusting the agent's natural semantic matching to pick tools.
2. Moving specialized skills (like science/bioinformatics) out of the global plugins directory and installing them ONLY in relevant project workspaces.
3. Keeping global skills absolutely minimal.

What is the optimal architecture for managing 70+ diverse skills across multiple disparate projects to minimize token usage while maximizing agent capability? Are there any risks to this proposed solution, and how should the user execute this transition?

---

## Advisor Responses

**The Contrarian (Response A):**
Trusting the agent’s "natural semantic matching" to pick from 70+ tools without explicit routing rules is a recipe for disaster. You are trading context window exhaustion for persistent hallucination and tool misfiring. An agent left to its own devices with a massive, uncurated toolbox will frequently select the wrong tool, loop endlessly trying to fix its own errors, and ultimately fail the task. Semantic matching sounds great until the agent decides to use a biological sequence aligner to process a marketing drip campaign because it saw the word "sequence."
Second, relying purely on project-specific plugins creates artificial silos. What happens when a marketing project needs to reference a data analysis tool you've buried in a "data-science" project? You'll find yourself duplicating plugins across workspaces, creating a maintenance nightmare when you inevitably need to update a skill's prompt. 
The fatal flaw here is the binary thinking: either load everything globally or isolate everything locally. The real solution isn't deleting your routing logic; it's dynamically injecting it. You need a metadata router—a lightweight global tool whose only job is to read the user's prompt, determine the required domain, and *then* dynamically load the necessary skill definitions into the context. Instead of forcing the agent to guess which tools are available locally, you abstract the tool catalog into an index. Stop trying to make the agent a mind reader. If you strip away the guardrails (the routing rules), the agent won't get smarter; it will just get lost faster.

**The First Principles Thinker (Response B):**
The fundamental issue isn't how to manage 70+ skills; it's why you are trying to manage 70+ skills in a single context window in the first place.
At a fundamental level, an LLM's context window is its working memory. Injecting bioinformatics tools into a marketing task is equivalent to forcing a copywriter to memorize a textbook on genome sequencing before writing a tweet. It degrades performance, wastes resources, and guarantees failure.
Your proposed solution correctly identifies the root cause: a monolithic architecture. You must move to scoped, context-aware environments. 
1. **Scoping is non-negotiable:** Skills must exist at the project level, not the global level. A workspace is a boundary of intent. If the intent is marketing, the tools available must be exclusively marketing.
2. **Manual routing is an anti-pattern:** "If task is X, use Y" rules are a brittle patch for an overloaded context window. If you scope the tools correctly per project, the LLM doesn't need explicit routing instructions; its natural semantic matching will select the right tool from a curated, small set. If it struggles to choose, your tool descriptions are flawed, not the routing logic.
3. **The Global Scope is a trap:** The global environment should contain zero specialized skills. It should only contain the mechanisms to create, manage, or navigate to specific projects.
The primary risk of your solution is holding on to the idea that you need a "master agent" that can do everything everywhere. Abandon that concept entirely. Build specialized environments for specialized tasks. Execute the transition by wiping the global config, establishing strict project boundaries, and installing plugins exclusively at the local level.

**The Executor (Response C):**
This proposed solution is 100% doable and the only practical way forward. Context limits are a hard technical constraint; you have to stop micromanaging the agent with massive routing lists. Here is exactly how you execute this on Monday morning:
1. **Nuke the Global File**: Open your global `user_rules.md` and delete the 70+ manual skill routing instructions. You are wasting tokens trying to manually wire up tools that the LLM is already designed to semantically match.
2. **Segregate the Heavy Lifters**: Move the massive `science` plugin out of `C:\Users\infon\.gemini\config\plugins` immediately. Put it inside the specific project folder where you actually do bioinformatics work (e.g., `[Project]\.gemini\plugins`).
3. **Localize Project Skills**: Do the same for marketing. If a skill is only for SyncMaster, move it to `syncmaster-marketing-1.0\.agents\skills`.
4. **Strip Global to the Bone**: Your global config should only contain universal utilities (like a web scraper or search tool). Everything else goes local.
**Risks?** The only practical risk is starting a new project and the agent failing because it can't find a specialized tool. The fix is trivial: just copy the skill folder into the new project's local directory. 
**Next Steps**: Stop debating the theory. Create the project-level `.gemini\plugins` or `.agents\skills` directories, move the heavy folders out of the global path, and watch your token usage drop instantly. You can get this done in 15 minutes.

**The Outsider (Response D):**
Why on earth is a marketing project loading bioinformatics tools? If you're building a website, you don't need a DNA sequencer. You created a massive pile of unrelated tools and are now surprised the system is confused and exhausted.
Your proposed solution of "project-specific plugins" isn't some groundbreaking architecture; it's just how normal organization works. You don't keep your blender in the bathroom. Put the science tools in the science folder. Put the marketing tools in the marketing folder. Keep the global tools to things you actually use everywhere, like basic file editing.
However, your first step—deleting explicit routing rules and trusting the AI to just "guess" based on semantic matching—is a mistake. You are replacing a bloated set of rules with zero rules. If a project has 15 marketing tools and you ask it to "fix the text," and there are tools for `copy-editing`, `copywriting`, and `ai-seo`, the AI is going to guess wrong half the time without guidance. 
The explicit routing wasn't your problem. The problem was dumping 70 tools into one global bucket. 
**Execution:**
1. Group your tools by actual use case (Science, Marketing, Dev).
2. Assign those groups strictly to the relevant project folders.
3. **Keep** the manual routing rules ("If X, use Y"), but put them inside the project-specific instructions, not the global file. 
4. Stop trying to build a "god agent" that can simultaneously cure diseases and write tweets. Build focused workers.

**The Expansionist (Response E):**
The proposed project-specific architecture isn't just a fix for token limits—it's the foundation for infinite scaling. Right now you're worried about managing 70 skills. You should be asking: "How do I manage 7,000?"
By decoupling skills from the global prompt and trusting semantic matching, you are unlocking a modular, infinite-capacity agent ecosystem. If you don't have to define every skill globally, there is literally no limit to the number of specialized capabilities you can build, scrape, or generate. You can transition from a "swiss army knife" to a "just-in-time supply chain."
Here’s the massive upside you’re missing: dynamic skill loading. Don't just install skills into static project workspaces. Build a master "Skill Index" tool—a lightweight directory. Give your agent the ability to search this index, pull down the exact plugin it needs for a specific task, use it, and unload it. This means your agent can spin up specialized subagents on the fly equipped with highly niche toolsets (e.g., an AlphaFold subagent that only exists for 10 seconds to run one query).
To execute this transition: lean entirely into semantic discovery. Stop manually mapping tasks. Instead, spend your effort generating hyper-specific, richly detailed `SKILL.md` descriptions so the LLM's natural routing becomes flawless. Turn your "marketing skills" and "bioinformatics plugins" into standalone repositories.
You are treating this as a token-reduction exercise. It's actually the moment your system graduates from a constrained personal assistant to an unbounded, autonomous agency. Go bigger.

---

## Chairman's Synthesis

### Where the Council Agrees
- **Scoping is non-negotiable:** The core issue is the global monolithic architecture. Injecting bioinformatics tools into a marketing task exhausts the context window and degrades performance. 
- **De-globalize:** The heavy specialized tools (especially the `science` plugin) must be immediately removed from the global `C:\Users\infon\.gemini\config\plugins` folder and installed locally at the project level. 

### Where the Council Clashes
- **Semantic Matching vs Explicit Routing:** The original proposal suggested deleting manual routing rules entirely and trusting the agent to pick the right tool natively. Several advisors violently disagreed, noting that if an agent has multiple similar tools locally (like `copywriting` and `copy-editing`), relying purely on "guessing" will cause hallucinations and misfires. 
- **The verdict:** Keep explicit routing rules, but move them from the global file to the local project files (e.g., `GEMINI.md` or `.agents/AGENTS.md`).

### Blind Spots the Council Caught
- **Physical vs Text Updates:** The peer reviewers caught that merely deleting the text routing rules in the global config won't actually stop the skills from loading if the plugin folders still live in `.gemini/config/plugins`. The physical folders must be moved.
- **Cross-Domain Needs:** Reviewers pointed out that if you strictly silo tools, you might run into issues when a marketing task requires a science tool. The solution is not to duplicate the tool, but to use **Subagent Delegation** (invoking a specialized science subagent from the marketing workspace).
- **Over-engineering:** The Expansionist's idea for a "Dynamic Skill Index" was universally panned by reviewers as introducing massive latency and recreating the exact context problem we are trying to solve. 

### The Recommendation
Adopt a **Project-Scoped Hybrid Architecture**. 
Do not trust pure semantic matching. Instead, group your tools by domain, install them locally in their respective projects, and migrate the manual routing rules into the local project instructions. 
1. The global config should be stripped to universal utilities. 
2. The `science` plugin must be moved to the local `.gemini/plugins` of your bioinformatics projects.
3. Marketing skills should reside in `syncmaster-marketing-1.0\.agents\skills`.
4. The manual routing rules currently in `user_global` should be cut and pasted into `GEMINI.md` or `AGENTS.md` in the SyncMaster workspace.

### The One Thing to Do First
Physically cut the `science` folder from `C:\Users\infon\.gemini\config\plugins` and paste it into the local plugin directory of whatever project actually requires it.
