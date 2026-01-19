
# Architecture

## 1. Purpose of This Document

This document describes the current architecture of **Oracle** — a Python tool for syllable counting and metrical analysis of English poetry using the CMU Pronouncing Dictionary.

It serves three main purposes:

- to record **why** certain design decisions were made (especially important in a solo/learning project where memory fades quickly)
- to make future refactoring or feature additions easier by providing context
- to serve as a self-reflection and portfolio artifact showing architectural thinking

Last updated: January 2026

## 2. Initial Design and Constraints

**Starting point (late 2025):**
- Very simple goal: read .txt poem files → count syllables per line → write basic analysis
- No prior experience writing maintainable medium-sized Python projects
- Strong preference for planning on paper first, then coding
- Constraints:
  - Use only standard library + Poetry + pytest + NLTK (CMUdict)
  - Keep it CLI-based, no web/UI
  - Maximize learning: try dataclasses, cached properties, TDD-ish approach, good test coverage

## 3. Evolution of the Architecture

### 3.1 From String-Based Processing to Domain Objects

**Before November 24('Implementation of Poem dataclass' commit):**
- Everything done with strings and functions operating on strings
- Simple but inflexible:
  - No clear structure for poems, stanzas, lines, words
  - Hard to extend for new features (e.g., rhyme detection, variant syllable counts)
  - Code duplication and tangled logic
- Adding any new feature would require extra work and risk of breaking existing code

**Trigger for change:**
- Realized that future features (rhyme schemes, stress patterns, multiple pronunciation handling) need to reason about words/lines/stanzas as **objects**, not substrings
- Wanted to separate "what is a poem structurally" from "how do I analyze it"

**Change:**
- Introduced domain model: `Poem → list[Stanza] → list[Line] → list[Word]`
- Used `@dataclass` + `@cached_property` for clean, efficient access

**Outcome:**
- Much easier to reason about individual parts
- Tests became more focused and readable
- Adding new analysis dimensions became possible without breaking existing code

### 3.2 Separation of Parsing, Analysis, and Output

**After (current):**
- `parser.py` — only responsible for turning raw text into `Poem` object (title skipping, blank-line stanza detection)
- `analyzer.py` — takes `Poem`, walks domain objects, computes metrics
- `main.py` + `write_poem_analysis` — I/O and formatting
- `syllable_counter.py` — isolated phonetic + fallback logic

**Outcome:**
- Each module has single responsibility
- Easier to test in isolation
- Clearer mental model when adding features

## 4. Current Architectural Overview

poems/*.txt 
  → read_poem_folder_and_return_names()
  → write_poem_analysis() 
  → Poem(text, filepath)
  → parse_into_stanzas() → list[Stanza]
  → analyze_poem() → metrics dict
  → write analysis.txt



Core layers:
- **Domain layer** — `Poem`, `Stanza`, `Line`, `Word` (dataclasses)
- **Infrastructure layer** — file reading/writing, CLI batch processing
- **Analysis layer** — syllable counting, future: meter/rhyme detection

## 5. Key Architectural Decisions

### ADR-001: Introducing Domain Objects
- **Context**  
  Switching from string-based operations to working with dataclasses

- **Decision**  
  Implementing `Poem > Stanza > Line > Word` data structure using `@dataclass` and `@cached_property`

- **Rationale**  
  - String operations became insufficient for future expansions (rhyme schemes, stress patterns, multiple pronunciation variants)  
  - Wanted to write analysis per stanza/line/word independently  
  - dataclasses provide clean syntax, type hints, and are easy to test

- **Consequences**  
  - Positive: modularity, better testability, easier to add features (e.g. `get_all_syllable_variants()`)  
  - Negative: slightly more code upfront, small performance overhead (acceptable for this scale)  
  - Allowed splitting `get_total_syllables()` and `get_all_syllable_variants()` instead of union return types

### ADR-002: Test-Informed Development Instead of Strict TDD
- **Context**  
  Wanted high test coverage but found pure TDD (write test → red → implement → green → refactor) too rigid during learning phase

- **Decision**  
  Mostly "test after" + "test during" approach:  
  - Write core logic first (often on paper → code)  
  - Write comprehensive tests immediately after (or in parallel for tricky parts)  
  - Use tests to explore edge cases and document behavior

- **Rationale**  
  - Learning phase — strict TDD felt like fighting the language  
  - Tests written after still catch regressions and force cleaner APIs  
  - High coverage (>85–90%) achieved without burning out

- **Consequences**  
  - Positive: good coverage, confidence in refactoring (e.g. domain split)  
  - Negative: some tests written later are integration-style instead of pure unit  
  - Acceptable tradeoff for first medium-sized project


### ADR-003: Splitting Syllable Methods Instead of Union Return Types

- **Context**  
  `get_total_syllables(use_all_variants)` returned `int | list[list[int]]` → caused mypy pain and unclear caller code

- **Decision**  
  Split into two public methods with `get_syllable_counts()` as shared implementation:
  - `get_total_syllables() → int` (public)
  - `get_all_syllable_variants() → list[list[int]]` (public)
  - `get_syllable_counts(use_all_variants) → list[int] | list[list[int]]` (internal helper)

- **Rationale**  
  Callers get clean, single-purpose methods without union types. The complexity of the union return lives in one internal method instead of spreading through the codebase.

- **Consequences**  
  Public API is simpler and more type-safe. Internal implementation can change without affecting callers. Slightly more methods, but each has clear intent.

## 6. Testing and Validation Strategy

- pytest + comprehensive assertions on structure, content, edge cases
- Focus: unit tests for domain objects & syllable counter, integration for parsing & full analysis flow
- Goal: >85% coverage on core logic
- No mocking of external libs (NLTK) — accept it as trusted dependency
- tmp_path fixture for all file I/O tests


## 7. Tradeoffs and Known Limitations

- English-only (CMUdict) — intentional scope limitation
- No support for multiple pronunciation selection yet (uses first variant)
- No rhyme/stress pattern detection (planned)
- Performance not optimized (irrelevant for <1000 poems)
- No CLI arguments yet (folder hardcoded with default)
- NLTK download required — documented in README

## 8. Future Considerations

- Add CLI arguments (`argparse` or `typer`): folder, output format (txt/json), options (variants on/off)
- Support multiple pronunciation variants + best-fit meter detection
- Rhyme scheme detection (end-word phoneme comparison)