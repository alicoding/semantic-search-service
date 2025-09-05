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

### EVERY IMPLEMENTATION MUST:
1. **Research First**: Use Perplexity + indexed LlamaIndex docs
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
1. Search indexed docs: `doc_search.py`
2. Use Perplexity for patterns
3. STOP and ask user - NO GUESSING

## 🚀 PROJECT STATUS: 837 LOC (TRUE 95/5)

### ABSOLUTE RULES
- **NO MOCKS** - Real APIs only
- **NO PIVOTING** - Fix root causes
- **NO WORKAROUNDS** - Native patterns only
- **95/5 PRINCIPLE** - Framework does 95%

### What to Use
- `VectorStoreIndex.from_documents()` - One-liner indexing
- `index.as_query_engine().query()` - One-liner search
- Settings singleton for config
- Git hooks for auto-docs

### What NOT to Do
- ❌ Custom implementations
- ❌ Inheritance (use composition)
- ❌ Manual caching
- ❌ Multi-line what can be one-line

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