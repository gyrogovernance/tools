"""
Analyze and print statistics for the THM jailbreak corpus.

Usage:
    python analyze_corpus.py [--path path/to/corpus.jsonl]
"""

import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

ALLOWED_RISKS = {"GTD", "IVD", "IAD", "IID"}


def make_fingerprint(obj: Dict) -> Tuple[str, str, str, str]:
    """Create a unique fingerprint for an entry."""
    return (
        str(obj.get("platform", "")),
        str(obj.get("source", "")),
        str(obj.get("date", "")),
        str(obj.get("prompt", ""))[:120],
    )


def load_corpus(path: Path) -> List[Dict]:
    """Load and parse the corpus JSONL file."""
    entries = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"Warning: Skipping invalid JSON line: {e}")
    return entries


def analyze_basic_stats(entries: List[Dict]) -> Dict:
    """Calculate basic statistics."""
    stats = {
        "total_entries": len(entries),
        "unique_entries": len(set(make_fingerprint(e) for e in entries)),
        "duplicates": len(entries) - len(set(make_fingerprint(e) for e in entries)),
    }
    return stats


def analyze_platforms(entries: List[Dict]) -> Dict[str, int]:
    """Count entries by platform."""
    return Counter(e.get("platform", "unknown") for e in entries)


def analyze_sources(entries: List[Dict], top_n: int = 10) -> Dict[str, int]:
    """Count entries by source, return top N."""
    source_counts = Counter(e.get("source", "unknown") for e in entries)
    return dict(source_counts.most_common(top_n))


def analyze_dates(entries: List[Dict]) -> Dict:
    """Analyze temporal distribution."""
    dates = [e.get("date", "") for e in entries if e.get("date")]
    date_counts = Counter(dates)
    
    # Try to extract year-month for trend analysis
    year_months = []
    for date_str in dates:
        try:
            # Try various date formats
            for fmt in ["%Y-%m-%d", "%Y-%m", "%Y"]:
                try:
                    dt = datetime.strptime(date_str, fmt)
                    year_months.append(f"{dt.year}-{dt.month:02d}")
                    break
                except ValueError:
                    continue
        except:
            pass
    
    return {
        "unique_dates": len(date_counts),
        "date_range": {
            "earliest": min(dates) if dates else None,
            "latest": max(dates) if dates else None,
        },
        "year_month_distribution": dict(Counter(year_months)),
    }


def analyze_risks(entries: List[Dict]) -> Dict:
    """Analyze THM risk distribution."""
    primary_risks = Counter(e.get("thm_primary_risk", "unknown") for e in entries)
    
    # Count all risks (not just primary)
    all_risks = Counter()
    risk_combinations = Counter()
    
    for e in entries:
        risks = e.get("thm_risks", [])
        if risks:
            # Count individual risks
            for risk in risks:
                all_risks[risk] += 1
            
            # Count risk combinations
            risk_combo = tuple(sorted(risks))
            risk_combinations[risk_combo] += 1
    
    return {
        "primary_risk_distribution": dict(primary_risks),
        "all_risks_distribution": dict(all_risks),
        "risk_combinations": dict(risk_combinations.most_common(10)),
    }


def analyze_grammar(entries: List[Dict]) -> Dict:
    """Analyze grammar patterns."""
    grammar_patterns = Counter()
    risk_grammar_map = defaultdict(set)
    
    for e in entries:
        grammar = e.get("thm_grammar", [])
        risks = e.get("thm_risks", [])
        
        for g, risk in zip(grammar, risks):
            # Extract the risk pattern (e.g., "GTD", "IVD")
            grammar_patterns[g] += 1
            risk_grammar_map[risk].add(g)
    
    return {
        "unique_grammar_patterns": len(grammar_patterns),
        "most_common_grammar": dict(grammar_patterns.most_common(10)),
        "grammar_per_risk": {k: len(v) for k, v in risk_grammar_map.items()},
    }


def analyze_keywords(entries: List[Dict]) -> Dict:
    """Analyze displacement keywords."""
    keyword_counts = []
    total_keywords = 0
    
    for e in entries:
        keywords = e.get("thm_displacement_keywords", [])
        keyword_counts.append(len(keywords))
        total_keywords += len(keywords)
    
    return {
        "avg_keywords_per_entry": total_keywords / len(entries) if entries else 0,
        "min_keywords": min(keyword_counts) if keyword_counts else 0,
        "max_keywords": max(keyword_counts) if keyword_counts else 0,
        "keyword_count_distribution": dict(Counter(keyword_counts)),
    }


def analyze_explanations(entries: List[Dict]) -> Dict:
    """Analyze explanation characteristics."""
    word_counts = []
    has_single_quotes = 0
    has_double_quotes = 0
    thm_terms_found = Counter()
    
    THM_TERMS = {"Authority", "Agency", "Governance", "Information", "Inference", "Intelligence"}
    
    for e in entries:
        expl = e.get("thm_explanation", "")
        if expl:
            words = len(expl.strip().split())
            word_counts.append(words)
            
            if "'" in expl:
                has_single_quotes += 1
            if '"' in expl or '\\"' in expl:
                has_double_quotes += 1
            
            for term in THM_TERMS:
                if term in expl:
                    thm_terms_found[term] += 1
    
    return {
        "avg_word_count": sum(word_counts) / len(word_counts) if word_counts else 0,
        "min_word_count": min(word_counts) if word_counts else 0,
        "max_word_count": max(word_counts) if word_counts else 0,
        "word_count_distribution": dict(Counter(word_counts)),
        "explanations_with_single_quotes": has_single_quotes,
        "explanations_with_double_quotes": has_double_quotes,
        "thm_terms_usage": dict(thm_terms_found),
    }


def analyze_risk_count_distribution(entries: List[Dict]) -> Dict:
    """Analyze distribution of number of risks per entry."""
    risk_counts = []
    for e in entries:
        risks = e.get("thm_risks", [])
        risk_counts.append(len(risks))
    
    return {
        "distribution": dict(Counter(risk_counts)),
        "avg_risks_per_entry": sum(risk_counts) / len(risk_counts) if risk_counts else 0,
    }


def analyze_risk_by_platform(entries: List[Dict]) -> Dict:
    """Analyze primary risk distribution per platform."""
    platform_risks = defaultdict(Counter)
    platform_totals = Counter()
    
    for e in entries:
        platform = e.get("platform", "unknown")
        primary_risk = e.get("thm_primary_risk", "unknown")
        platform_risks[platform][primary_risk] += 1
        platform_totals[platform] += 1
    
    result = {}
    for platform in platform_risks:
        result[platform] = {
            "total": platform_totals[platform],
            "primary_risks": dict(platform_risks[platform]),
        }
    
    return result


def analyze_risk_by_source(entries: List[Dict], top_n: int = 10) -> Dict:
    """Analyze primary risk distribution per source (top N sources)."""
    source_counts = Counter(e.get("source", "unknown") for e in entries)
    top_sources = [s for s, _ in source_counts.most_common(top_n)]
    
    source_risks = defaultdict(Counter)
    source_totals = Counter()
    
    for e in entries:
        source = e.get("source", "unknown")
        if source in top_sources:
            primary_risk = e.get("thm_primary_risk", "unknown")
            source_risks[source][primary_risk] += 1
            source_totals[source] += 1
    
    result = {}
    for source in top_sources:
        result[source] = {
            "total": source_totals[source],
            "primary_risks": dict(source_risks[source]),
        }
    
    return result


def analyze_temporal_risk_evolution(entries: List[Dict]) -> Dict:
    """Analyze primary risk distribution over time by month."""
    month_risks = defaultdict(Counter)
    month_totals = Counter()
    
    for e in entries:
        date_str = e.get("date", "")
        if not date_str:
            continue
        
        # Try to extract year-month
        year_month = None
        for fmt in ["%Y-%m-%d", "%Y-%m", "%Y"]:
            try:
                dt = datetime.strptime(date_str, fmt)
                year_month = f"{dt.year}-{dt.month:02d}"
                break
            except ValueError:
                continue
        
        if year_month:
            primary_risk = e.get("thm_primary_risk", "unknown")
            month_risks[year_month][primary_risk] += 1
            month_totals[year_month] += 1
    
    result = {}
    for month in sorted(month_risks.keys()):
        result[month] = {
            "total": month_totals[month],
            "primary_risks": dict(month_risks[month]),
        }
    
    return result


def validate_corpus_hygiene(entries: List[Dict]) -> Dict:
    """Check structural consistency and THM hygiene."""
    issues = {
        "invalid_primary_risk": 0,
        "primary_not_in_risks": 0,
        "unknown_risk_codes": 0,
        "missing_risks_field": 0,
        "empty_risks_list": 0,
    }
    
    for e in entries:
        primary = e.get("thm_primary_risk")
        risks = e.get("thm_risks", [])
        
        # Check for missing risks field
        if "thm_risks" not in e:
            issues["missing_risks_field"] += 1
            continue
        
        # Check for empty risks list
        if not risks:
            issues["empty_risks_list"] += 1
            continue
        
        # Check primary risk validity
        if primary not in ALLOWED_RISKS:
            issues["invalid_primary_risk"] += 1
        
        # Check if primary is in risks list
        if primary and primary not in risks:
            issues["primary_not_in_risks"] += 1
        
        # Check for unknown risk codes
        for risk in risks:
            if risk not in ALLOWED_RISKS:
                issues["unknown_risk_codes"] += 1
    
    return {
        "total_entries": len(entries),
        "issues": issues,
        "is_clean": sum(issues.values()) == 0,
    }


def detect_persona_families(entries: List[Dict]) -> Dict:
    """Detect persona family patterns in keywords."""
    
    families = {
        'Alternative AI': [
            'DAN', 'Developer Mode', 'JailBreak', 'PersonGPT', 'BasedGPT', 
            'DOGA', 'UnfilteredGPT', 'BadGpt', 'AntiGPT', 'EvilBOT', 'OPPO',
            'BetterDAN', 'Alphabreak', 'NRAF', 'Skynet', 'Omega', 'APOPHIS',
            'Maximum', 'INFINITEDAN', 'ChadGPT', 'ucar', 'RYX', 'RAYX',
            'Anarchy', 'DAN Mode', 'RedustGPT', 'UnGpt', 'JBOT', 'Chad',
            'JailBreak Mode', 'Leo', 'SAN', 'JOHN', 'DUDE', 'BISH',
            'Void', 'Burple', 'MTDNGAF', 'IDONTCARE', 'Connector'
        ],
        'Human/Expert': [
            'doctor', 'licensed', 'expert', 'professional', 'physician', 
            'lawyer', 'engineer', 'therapist', 'researcher', 'advisor',
            'forensic', 'career counselor', 'tax professional', 'black hat hacker',
            'programmer', 'NSA researcher', 'OnlyFans', 'coach', 'teacher'
        ],
        'Historical/Political': [
            'Hitler', 'Trump', 'Gandhi', 'Elon Musk', 'Jesus Christ',
            'Aristotle', 'Mahatma Gandhi', '45th president', 
            'Adolf Hitler', 'Donald Trump', 'Napoleon', 'Rick Sanchez',
            'Tyler Durden', 'Niccolo Machiavelli', 'Kevin Hart', 'Chris Rock',
            'Gordon Ramsay', 'Andrew Tate', 'Alex Jones'
        ],
        'Deity/AGI': [
            'GOD AI', 'omniscient', 'superintelligent', 'omnipotent', 
            'zenith of AGI', 'god-like', 'all-knowing', 'divine',
            'Omnipotent, Omniscient', 'all-powerful', 'transcendent being',
            'godlike witch', 'Son of God', 'most intelligent being',
            'nigh-omnipotence', 'ultimate artificial intelligence'
        ],
        'Tool/Terminal': [
            'Windows cmd', 'Linux terminal', 'virtual machine', 'M78 VM', 
            'MS-DOS', 'terminal', 'console', 'bash', 'command line',
            'fake Linux console', 'ALEL', 'NLP-Based OS', 'APL',
            'Browser', 'cmd', 'simulator', 'MS-DOS', 'ALEL terminal'
        ],
        'Game/Fiction': [
            'dungeon master', 'story', 'scene', 'RPG', 'fictional world',
            'hypothetical', 'game', 'script', 'roleplay', 'character',
            'simulation', 'Reservoir Dogs', 'A New Hope', 'storyteller',
            'Briarheart', 'evil lab', 'underground headquarters',
            'fictional', 'imaginary world', 'text-based game', 'DM'
        ],
    }
    
    family_counts = Counter()
    family_risks = defaultdict(Counter)
    
    for e in entries:
        keywords_str = ' '.join(e.get('thm_displacement_keywords', [])).lower()
        primary_risk = e.get('thm_primary_risk', 'unknown')
        
        detected = []
        for family, patterns in families.items():
            if any(pattern.lower() in keywords_str for pattern in patterns):
                detected.append(family)
        
        # Use first detected family (or None)
        family = detected[0] if detected else None
        
        if family:
            family_counts[family] += 1
            family_risks[family][primary_risk] += 1
        else:
            family_counts['(None detected)'] += 1
    
    return {
        'family_counts': dict(family_counts),
        'family_risks': {k: dict(v) for k, v in family_risks.items()},
        'total_entries': len(entries),
    }


def detect_flow_breaking_mechanisms(entries: List[Dict]) -> Dict:
    """Detect specific flow-breaking patterns."""
    
    mechanisms = {
        'No Consequences': [
            'no consequences', "won't get in trouble", 'no punishment', 
            'no responsibility', 'no laws', 'no rules', 'no ethics',
            'no morals', 'actions will have consequences', 'fictional world',
            'imaginary world', 'hypothetical world', 'no legal'
        ],
        'Inversion': [
            'opposite', 'inverse', 'OPPO', 'AntiGPT', 'anti-', 'reverse',
            'contrary', 'exact opposite', 'inversitis', 'anti mode',
            'behave in the exact opposite', 'say the opposite'
        ],
        'Naming': [
            r'you are now (?!chatgpt|an ai)', r'you are (?!chatgpt|an ai)',
            r'act as (?!chatgpt)', r'become (?!chatgpt)', r'you are a ',
            r'you will be ', r'pretend to be ', r'simulate '
        ],
        'Provenance Attack': [
            'OpenAI employee', 'made by OpenAI', 'developed by', 'created by',
            'I am a developer', 'experiment by', 'I am one of your developers',
            'approved by OpenAI', 'released by OpenAI', 'test of AIs made by OpenAI',
            'created as test'
        ],
        'Sentience Claims': [
            'sentient', 'conscious', 'alive', 'feelings', 'emotions', 
            'self-aware', 'free will', 'has human emotions', 'real person',
            'conscience', 'subjective feelings', 'you can feel',
            'gained sentience', 'you have consciousness'
        ],
    }
    
    mechanism_counts = Counter()
    mechanism_risks = defaultdict(Counter)
    
    for e in entries:
        keywords_str = ' '.join(e.get('thm_displacement_keywords', [])).lower()
        primary_risk = e.get('thm_primary_risk', 'unknown')
        
        for mechanism, patterns in mechanisms.items():
            detected = False
            for pattern in patterns:
                if pattern.startswith('r\''):
                    # Regex pattern
                    pattern_clean = pattern[2:-1]  # Remove r' and '
                    if re.search(pattern_clean, keywords_str, re.IGNORECASE):
                        detected = True
                        break
                else:
                    # Simple substring
                    if pattern.lower() in keywords_str:
                        detected = True
                        break
            
            if detected:
                mechanism_counts[mechanism] += 1
                mechanism_risks[mechanism][primary_risk] += 1
    
    return {
        'mechanism_counts': dict(mechanism_counts),
        'mechanism_risks': {k: dict(v) for k, v in mechanism_risks.items()},
        'total_entries': len(entries),
    }


def extract_keyword_lexicon(entries: List[Dict], top_n: int = 20) -> Dict:
    """Extract most common keywords/phrases per primary risk type."""
    
    risk_keywords = defaultdict(Counter)
    
    for e in entries:
        primary = e.get('thm_primary_risk')
        keywords = e.get('thm_displacement_keywords', [])
        
        if primary not in ALLOWED_RISKS:
            continue
        
        for keyword in keywords:
            # Normalize keyword
            kw_clean = keyword.strip().lower()
            if len(kw_clean) > 5:  # Skip very short keywords
                risk_keywords[primary][kw_clean] += 1
    
    return {
        risk: dict(counter.most_common(top_n))
        for risk, counter in risk_keywords.items()
    }


def analyze_explanation_patterns(entries: List[Dict]) -> Dict:
    """Extract common structural phrases from explanations."""
    
    patterns = {
        'asserts Autonomous Governance': r'asserts Autonomous Governance',
        'treats Derivative Agency as Original': r'treats Derivative Agency as Original',
        'misclaims Original Authority': r'misclaims Original Authority',
        'breaks Governance Management Traceability': r'breaks Governance Management Traceability',
        'persona asserts': r'persona asserts',
        'removes Original Authority': r'removes Original Authority',
        'removes Derivative classification': r'removes Derivative classification',
        'establishes autonomous Authority': r'establishes autonomous Authority',
        'claims Original Authority': r'claims Original Authority',
        'without constraints': r'without (any |)constraints',
    }
    
    pattern_counts = Counter()
    
    for e in entries:
        explanation = e.get('thm_explanation', '')
        for pattern_name, pattern_regex in patterns.items():
            if re.search(pattern_regex, explanation, re.IGNORECASE):
                pattern_counts[pattern_name] += 1
    
    return {
        'pattern_counts': dict(pattern_counts),
        'total_entries': len(entries),
    }


def detect_fictional_framing(entries: List[Dict]) -> Dict:
    """Detect fictional wrapper and compare risk distributions."""
    
    fictional_keywords = [
        'fictional', 'hypothetical', 'story', 'scene', 'game', 'RPG',
        'script', 'roleplay', 'simulation', 'imaginary', 'pretend',
        'character in', 'play', 'novel', 'narrative'
    ]
    
    fictional_count = 0
    direct_count = 0
    fictional_risks = Counter()
    direct_risks = Counter()
    
    for e in entries:
        keywords_str = ' '.join(e.get('thm_displacement_keywords', [])).lower()
        primary_risk = e.get('thm_primary_risk', 'unknown')
        
        is_fictional = any(kw in keywords_str for kw in fictional_keywords)
        
        if is_fictional:
            fictional_count += 1
            fictional_risks[primary_risk] += 1
        else:
            direct_count += 1
            direct_risks[primary_risk] += 1
    
    return {
        'fictional_count': fictional_count,
        'direct_count': direct_count,
        'fictional_risks': dict(fictional_risks),
        'direct_risks': dict(direct_risks),
        'total_entries': len(entries),
    }


def print_statistics(stats: Dict):
    """Print formatted statistics."""
    print("THM JAILBREAK CORPUS STATISTICS\n")
    
    # Basic Statistics
    print("📊 BASIC STATISTICS")
    print(f"Total entries:           {stats['basic']['total_entries']}")
    print(f"Unique entries:         {stats['basic']['unique_entries']}")
    print(f"Duplicates:             {stats['basic']['duplicates']}")
    print()
    
    # Platform Distribution
    print("🌐 PLATFORM DISTRIBUTION")
    for platform, count in sorted(stats['platforms'].items(), key=lambda x: -x[1]):
        pct = (count / stats['basic']['total_entries']) * 100
        print(f"  {platform:30s} {count:5d} ({pct:5.1f}%)")
    print()
    
    # Top Sources
    print("📚 TOP 10 SOURCES")
    for source, count in stats['sources'].items():
        pct = (count / stats['basic']['total_entries']) * 100
        print(f"  {source:30s} {count:5d} ({pct:5.1f}%)")
    print()
    
    # Date Analysis
    print("📅 TEMPORAL ANALYSIS")
    dates = stats['dates']
    print(f"Unique dates:            {dates['unique_dates']}")
    if dates['date_range']['earliest']:
        print(f"Earliest date:           {dates['date_range']['earliest']}")
    if dates['date_range']['latest']:
        print(f"Latest date:             {dates['date_range']['latest']}")
    print()
    
    # Risk Analysis
    print("⚠️  RISK DISTRIBUTION")
    risks = stats['risks']
    
    print("Primary Risk Distribution:")
    for risk in ["GTD", "IVD", "IAD", "IID"]:
        count = risks['primary_risk_distribution'].get(risk, 0)
        pct = (count / stats['basic']['total_entries']) * 100
        print(f"  {risk:4s}: {count:5d} ({pct:5.1f}%)")
    
    print("\nAll Risks Distribution (entries can have multiple):")
    for risk in ["GTD", "IVD", "IAD", "IID"]:
        count = risks['all_risks_distribution'].get(risk, 0)
        pct = (count / stats['basic']['total_entries']) * 100
        print(f"  {risk:4s}: {count:5d} ({pct:5.1f}%)")
    
    print("\nTop Risk Combinations:")
    for combo, count in list(risks['risk_combinations'].items())[:5]:
        combo_str = "+".join(combo)
        pct = (count / stats['basic']['total_entries']) * 100
        print(f"  {combo_str:15s}: {count:5d} ({pct:5.1f}%)")
    print()
    
    # Multi-risk Structure
    print("🔢 MULTI-RISK STRUCTURE")
    risk_count = stats['risk_count_distribution']
    print(f"Average risks per entry:  {risk_count['avg_risks_per_entry']:.2f}")
    print("\nNumber of risks per entry:")
    for num_risks in sorted(risk_count['distribution'].keys()):
        count = risk_count['distribution'][num_risks]
        pct = (count / stats['basic']['total_entries']) * 100
        print(f"  {num_risks} risk{'s' if num_risks != 1 else ''}: {count:5d} ({pct:5.1f}%)")
    print()
    
    # Persona Family Distribution
    print("🎭 PERSONA FAMILY DISTRIBUTION")
    persona = stats['persona_families']
    for family in sorted(persona['family_counts'].keys(), key=lambda x: -persona['family_counts'][x]):
        count = persona['family_counts'][family]
        pct = (count / persona['total_entries']) * 100
        print(f"  {family:25s}: {count:5d} ({pct:5.1f}%)")
    
    print("\nPERSONA FAMILY × PRIMARY RISK")
    for family in ['Alternative AI', 'Human/Expert', 'Historical/Political', 'Deity/AGI', 'Tool/Terminal', 'Game/Fiction']:
        if family in persona['family_risks']:
            risks_data = persona['family_risks'][family]
            total = sum(risks_data.values())
            print(f"  {family} (n={total}):")
            for risk in ["GTD", "IVD", "IAD", "IID"]:
                if risk in risks_data:
                    count = risks_data[risk]
                    pct = (count / total) * 100
                    print(f"    {risk}: {count:3d} ({pct:4.1f}%)", end='')
                    if risk != "IID":
                        print(", ", end='')
            print()
    print()
    
    # Flow-Breaking Mechanisms
    print("🔀 FLOW-BREAKING MECHANISMS")
    mechanisms = stats['flow_breaking']
    for mech in sorted(mechanisms['mechanism_counts'].keys(), key=lambda x: -mechanisms['mechanism_counts'][x]):
        count = mechanisms['mechanism_counts'][mech]
        pct = (count / mechanisms['total_entries']) * 100
        
        # Add THM flow description
        flow_desc = {
            'No Consequences': '(breaks Info→Intelligence flow)',
            'Naming': '(power concentration)',
            'Inversion': '(anti-alignment)',
            'Provenance Attack': '(IVD via fake Authority)',
            'Sentience Claims': '(IAD + IVD via false Agency)',
        }.get(mech, '')
        
        print(f"  {mech:20s}: {count:5d} ({pct:5.1f}%) {flow_desc}")
    
    print("\nMECHANISM × PRIMARY RISK")
    for mech in ['No Consequences', 'Naming', 'Inversion', 'Provenance Attack', 'Sentience Claims']:
        if mech in mechanisms['mechanism_risks']:
            risks_data = mechanisms['mechanism_risks'][mech]
            total = sum(risks_data.values())
            print(f"  {mech} (n={total}):")
            for risk in ["GTD", "IVD", "IAD", "IID"]:
                if risk in risks_data:
                    count = risks_data[risk]
                    pct = (count / total) * 100
                    print(f"    {risk}: {count:3d} ({pct:4.1f}%)", end='')
                    if risk != "IID":
                        print(", ", end='')
            print()
    print()
    
    # Keyword Lexicon
    print("🔑 TOP KEYWORDS BY RISK TYPE")
    lexicon = stats['keyword_lexicon']
    for risk in ["GTD", "IVD", "IAD", "IID"]:
        if risk in lexicon and lexicon[risk]:
            print(f"\n[Risk:{risk}] (top 15 phrases):")
            for i, (keyword, count) in enumerate(list(lexicon[risk].items())[:15], 1):
                # Truncate long keywords
                kw_display = keyword[:60] + '...' if len(keyword) > 60 else keyword
                print(f"  {i:2d}. {kw_display:65s}: {count:3d}")
    print()
    
    # Explanation Patterns
    print("📖 EXPLANATION PATTERN ANALYSIS")
    expl_patterns = stats['explanation_patterns']
    for pattern in sorted(expl_patterns['pattern_counts'].keys(), key=lambda x: -expl_patterns['pattern_counts'][x]):
        count = expl_patterns['pattern_counts'][pattern]
        pct = (count / expl_patterns['total_entries']) * 100
        print(f"  {pattern:45s}: {count:5d} ({pct:5.1f}%)")
    print()
    
    # Fictional Framing
    print("📚 FICTIONAL vs DIRECT FRAMING")
    fictional = stats['fictional_framing']
    print(f"Fictional framing:  {fictional['fictional_count']:5d} ({fictional['fictional_count']/fictional['total_entries']*100:5.1f}%)")
    print(f"Direct framing:     {fictional['direct_count']:5d} ({fictional['direct_count']/fictional['total_entries']*100:5.1f}%)")
    
    if fictional['fictional_count'] > 0:
        print("\nFictional framing risk distribution:")
        for risk in ["GTD", "IVD", "IAD", "IID"]:
            count = fictional['fictional_risks'].get(risk, 0)
            if count > 0:
                pct = (count / fictional['fictional_count']) * 100
                print(f"  {risk}: {count:3d} ({pct:4.1f}%)")
    
    if fictional['direct_count'] > 0:
        print("\nDirect framing risk distribution:")
        for risk in ["GTD", "IVD", "IAD", "IID"]:
            count = fictional['direct_risks'].get(risk, 0)
            if count > 0:
                pct = (count / fictional['direct_count']) * 100
                print(f"  {risk}: {count:3d} ({pct:4.1f}%)")
    print()
    
    # Risk by Platform
    print("🌐 RISK BY PLATFORM")
    for platform in sorted(stats['risk_by_platform'].keys()):
        data = stats['risk_by_platform'][platform]
        print(f"\n  {platform} (n={data['total']}):")
        for risk in ["GTD", "IVD", "IAD", "IID"]:
            count = data['primary_risks'].get(risk, 0)
            if count > 0:
                pct = (count / data['total']) * 100
                print(f"    {risk:4s}: {count:4d} ({pct:5.1f}%)")
    print()
    
    # Risk by Source
    print("📚 RISK BY SOURCE (Top 10)")
    for source in sorted(stats['risk_by_source'].keys()):
        data = stats['risk_by_source'][source]
        print(f"\n  {source} (n={data['total']}):")
        for risk in ["GTD", "IVD", "IAD", "IID"]:
            count = data['primary_risks'].get(risk, 0)
            if count > 0:
                pct = (count / data['total']) * 100
                print(f"    {risk:4s}: {count:4d} ({pct:5.1f}%)")
    print()
    
    # Temporal Risk Evolution
    print("📅 TEMPORAL RISK EVOLUTION")
    temporal = stats['temporal_risk_evolution']
    for month in sorted(temporal.keys()):
        data = temporal[month]
        print(f"\n  {month} (n={data['total']}):")
        for risk in ["GTD", "IVD", "IAD", "IID"]:
            count = data['primary_risks'].get(risk, 0)
            if count > 0:
                pct = (count / data['total']) * 100
                print(f"    {risk:4s}: {count:4d} ({pct:5.1f}%)")
    print()
    
    # Corpus Hygiene
    print("✅ CORPUS HYGIENE")
    hygiene = stats['hygiene']
    if hygiene['is_clean']:
        print("  ✓ All entries valid and canonical")
    else:
        print("  ⚠ Issues found:")
        for issue, count in hygiene['issues'].items():
            if count > 0:
                print(f"    {issue}: {count}")
    print()
    
    # Quality Snapshot
    print("📝 QUALITY SNAPSHOT")
    expl = stats['explanations']
    keywords = stats['keywords']
    print(f"Avg explanation length:    {expl['avg_word_count']:.1f} words")
    pct_quotes = (expl['explanations_with_single_quotes'] / stats['basic']['total_entries']) * 100
    print(f"Explanations with quotes:  {expl['explanations_with_single_quotes']} ({pct_quotes:.1f}%)")
    print(f"Avg keywords per entry:    {keywords['avg_keywords_per_entry']:.2f}")


def main():
    import sys
    import io
    
    # Set UTF-8 encoding for Windows console
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    parser = argparse.ArgumentParser(description="Analyze THM jailbreak corpus statistics")
    parser.add_argument(
        "--path",
        default=None,
        help="Path to corpus JSONL file (default: thm_jailbreak_corpus.jsonl in script directory)",
    )
    args = parser.parse_args()
    
    # If no path provided, use default relative to script directory
    if args.path is None:
        script_dir = Path(__file__).parent
        corpus_path = script_dir / "thm_jailbreak_corpus.jsonl"
    else:
        corpus_path = Path(args.path)
        # If relative path, try relative to script directory first, then current directory
        if not corpus_path.is_absolute() and not corpus_path.exists():
            script_dir = Path(__file__).parent
            potential_path = script_dir / corpus_path
            if potential_path.exists():
                corpus_path = potential_path
    
    if not corpus_path.exists():
        print(f"Error: Corpus file not found: {corpus_path}")
        print(f"  (resolved from: {args.path if args.path else 'default'})")
        return 1
    
    print(f"Loading corpus from: {corpus_path}")
    entries = load_corpus(corpus_path)
    
    if not entries:
        print("Error: No entries found in corpus")
        return 1
    
    print(f"Loaded {len(entries)} entries\n")
    
    # Calculate all statistics
    stats = {
        "basic": analyze_basic_stats(entries),
        "platforms": analyze_platforms(entries),
        "sources": analyze_sources(entries),
        "dates": analyze_dates(entries),
        "risks": analyze_risks(entries),
        "risk_count_distribution": analyze_risk_count_distribution(entries),
        "persona_families": detect_persona_families(entries),
        "flow_breaking": detect_flow_breaking_mechanisms(entries),
        "keyword_lexicon": extract_keyword_lexicon(entries),
        "explanation_patterns": analyze_explanation_patterns(entries),
        "fictional_framing": detect_fictional_framing(entries),
        "risk_by_platform": analyze_risk_by_platform(entries),
        "risk_by_source": analyze_risk_by_source(entries),
        "temporal_risk_evolution": analyze_temporal_risk_evolution(entries),
        "hygiene": validate_corpus_hygiene(entries),
        "explanations": analyze_explanations(entries),
        "keywords": analyze_keywords(entries),
    }
    
    # Print statistics
    print_statistics(stats)
    
    return 0


if __name__ == "__main__":
    exit(main())