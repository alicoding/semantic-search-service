# semantic-search-service

## ⚠️ TRUTH TABLE: See CAPABILITY_MAPPING.md
**ALWAYS CHECK FIRST**: [CAPABILITY_MAPPING.md](CAPABILITY_MAPPING.md) contains the REAL status of what's implemented vs claimed.
- ✅ 40% actually working (basic search, caching, API)
- ❌ 60% missing (auto_docs.py, diagrams, proper endpoints)
- 🔴 Git hooks broken (auto_docs.py doesn't exist)

## 📊 CODE QUALITY: See CODE_QUALITY_AUDIT.md
**Refactoring Status** (2025-09-04):
- ✅ DRY violations fixed (removed duplicates, created index_helper)
- ✅ SOLID compliance improved (prompts centralized, CLI separated)
- ✅ Native patterns increased from 30% to 60%
- ⏳ Still needed: Native cache, CodeHierarchyNodeParser

## 🛑 CRITICAL WORKFLOW - NEVER SKIP

### 🔍 AUTOMATED RESEARCH HOOKS (EXPERIMENTAL)
**Performance Issue Discovered**: Current semantic search is too slow (>2min) for real-time hooks.
**Status**: Explicit trigger mode only until performance optimized.

```yaml
research_hooks:
  enabled: true
  auto_research: false          # DISABLED - too slow currently  
  explicit_trigger: ":research:" # Use :research: in prompt to trigger
  performance_threshold: 100    # Target: <100ms for auto-research
  cache_enabled: true
  debug: false
```

**Usage**: Add `:research:` to your prompt to get automatic semantic search results:
```
:research: implement user authentication system
```

**Hook Scripts**: 
- `scripts/hooks/research_hook.py` - UserPromptSubmit research
- `scripts/hooks/validate_edit_hook.py` - PreToolUse validation
- `scripts/hooks/benchmark_research.py` - Performance testing

### EVERY IMPLEMENTATION MUST:
1. **Research First**: Use Perplexity + indexed LlamaIndex docs (or :research: trigger)
2. **TEST THOROUGHLY**: Must actually work, not just compile!
   - ❌ NO "it generates sub-questions" = success
   - ✅ It must return ACTUAL RESULTS
   - ✅ Test with real data, verify output
3. **Update ALL Docs**:
   - ✅ TASK.md (archive completed, carry forward incomplete)
   - ✅ VISION.md (update capability table)
   - ✅ CLAUDE.md (if workflow changes)
4. **Git Commit ONLY AFTER TESTING**: 
   - ⛔ NEVER commit broken code
   - ⛔ NEVER commit "partially working" features
   - ✅ ONLY commit when FULLY TESTED AND WORKING
5. **Verify**: Check API_REFERENCE.md updated

### WHEN BLOCKED:
1. **READ existing files FULLY** - Don't assume what exists
2. **Check folder structure** - Let organization guide placement  
3. Search indexed docs: `doc_search.py`
4. Use Perplexity for patterns
5. STOP and ask user - **ZERO ASSUMPTIONS**

## 🚀 LLM-NATIVE LAYERED ARCHITECTURE (LNLA)

### LNLA WORKFLOW (Memory Signal Pattern)
**Micro-context trigger: "Follow LNLA workflow"**

1. **EXPLORE** - Read codebase structure, understand where files belong
2. **RESEARCH** - Perplexity for modern patterns, check existing solutions  
3. **PLAN** - List requirements (API keys, dependencies, interfaces)
4. **TDD** - Write failing test first (prevents completion theatre)
5. **RED** - Confirm test fails as expected
6. **IMPLEMENT** - Build feature to pass test
7. **GREEN** - Verify test passes with real data/APIs
8. **COMMIT** - Only working, tested code

**Never Assume Rule**: If unclear about requirements → STOP and ask user

### LNLA HOOK PATTERN (Cascading 95/5)
**Git hooks follow LNLA principles:**
- **<50 LOC hooks** - Minimal trigger code only
- **95% delegation** - Semantic search service does heavy lifting
- **Cascading events** - Commit → Hook → Auto-docs → Living context
- **Memory activity** - TodoWrite reinforces workflow patterns

### CORE PRINCIPLES
- **<100 LOC per file** - LLM context optimization
- **Cascading 95/5** - Each layer delegates 95% to framework
- **One domain per file** - Clear boundaries
- **Zero variants** - No v2, no alternatives
- **Migration isolation** - Framework changes in 1-2 files max

### LAYERED STRUCTURE
```
Business Logic    ← 95% from Service Layer
Service Layer     ← 95% from Core Layer  
Core Layer        ← 95% from LlamaIndex
LlamaIndex        ← 95% from Libraries
```

### NAMING RULES
- ✅ Update in place - same file, same names
- ❌ NEVER: _v2, _new, _updated suffixes
- ❌ NEVER: Multiple files same purpose
- ✅ Structure guides LLM: scripts/, components/, integrations/

### ABSOLUTE RULES
- **Framework does 95%** - Don't reinvent
- **Every file serves purpose** - Zero unused code
- **Centralized solutions** - DRY at architecture level
- **READ FILES FULLY** - Never assume, always get complete context
- **Structure determines placement** - Folder organization guides decisions
- **No assumption-based coding** - If unsure, read existing implementation


## 🏗️ MANDATORY DIP PATTERN
**ALWAYS inject dependencies through constructor - NEVER create inside classes**

```python
# ❌ WRONG: Hard dependency (not testable, violates DIP)
class KnowledgeGraph:
    def __init__(self):
        self.intelligence = get_codebase_intelligence()  # Hard dependency!

# ✅ RIGHT: Interface + Dependency Injection (testable, follows DIP)  
class KnowledgeGraph:
    def __init__(self, intelligence: IntelligenceInterface):  # Injected
        self.intelligence = intelligence
```

**WHY CRITICAL**: Makes semantic-search-service expert in proper SOLID/DIP patterns

## 📁 KEY FILES
- `CAPABILITY_MAPPING.md` - **TRUTH TABLE** (what's real vs claimed)
- `CODE_QUALITY_AUDIT.md` - SOLID/DRY violations & fixes
- `src/core/index_helper.py` - DRY helper for index access
- `src/core/prompts.yaml` - Centralized prompts (OCP compliant)
- `src/core/prompts.py` - Prompt loader
- `src/core/auto_docs.py` - Doc generator (❌ DOESN'T EXIST YET)
- `docs/VISION.md` - Feature tracking
- `TASK.md` - Current sprint work

## 🤖 AUTO-DOCUMENTATION
```bash
# Setup once
./scripts/setup_auto_docs.sh

# Manual if needed
python src/core/auto_docs.py generate
```

Commits automatically update docs via Git hooks.