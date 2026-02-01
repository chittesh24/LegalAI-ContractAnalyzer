"""
Test script for Contract Analyzer
Validates core functionality
"""
import sys
from pathlib import Path
from contract_analyzer import ContractAnalyzer
from config import TEMPLATES_DIR


def test_document_parsing():
    """Test document parsing functionality"""
    print("\n" + "="*60)
    print("TEST 1: Document Parsing")
    print("="*60)
    
    analyzer = ContractAnalyzer()
    test_file = TEMPLATES_DIR / "sample_vendor_contract.txt"
    
    if not test_file.exists():
        print("❌ Test file not found!")
        return False
    
    print(f"✓ Testing with: {test_file.name}")
    
    try:
        result = analyzer.parser.parse_document(test_file)
        
        if result["success"]:
            print(f"✅ Parsing successful!")
            print(f"   - Word count: {result['word_count']}")
            print(f"   - Char count: {result['char_count']}")
            print(f"   - File type: {result['file_type']}")
            return True
        else:
            print(f"❌ Parsing failed: {result['error']}")
            return False
    
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False


def test_clause_extraction():
    """Test clause extraction"""
    print("\n" + "="*60)
    print("TEST 2: Clause Extraction")
    print("="*60)
    
    analyzer = ContractAnalyzer()
    test_file = TEMPLATES_DIR / "sample_vendor_contract.txt"
    
    try:
        parse_result = analyzer.parser.parse_document(test_file)
        text = parse_result["text"]
        
        clauses = analyzer.nlp.extract_clauses(text)
        
        print(f"✅ Extracted {len(clauses)} clauses")
        print(f"   Sample clause types: {set([c['type'] for c in clauses[:5]])}")
        
        if len(clauses) > 0:
            print(f"   First clause preview: {clauses[0]['text'][:100]}...")
            return True
        else:
            print("❌ No clauses extracted")
            return False
    
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False


def test_entity_extraction():
    """Test entity extraction"""
    print("\n" + "="*60)
    print("TEST 3: Entity Extraction")
    print("="*60)
    
    analyzer = ContractAnalyzer()
    test_file = TEMPLATES_DIR / "sample_vendor_contract.txt"
    
    try:
        parse_result = analyzer.parser.parse_document(test_file)
        text = parse_result["text"]
        
        entities = analyzer.nlp.extract_entities(text)
        
        print(f"✅ Entity extraction complete")
        print(f"   - Parties: {len(entities.get('parties', []))}")
        print(f"   - Dates: {len(entities.get('dates', []))}")
        print(f"   - Amounts: {len(entities.get('amounts', []))}")
        print(f"   - Locations: {len(entities.get('locations', []))}")
        
        if entities.get('parties'):
            print(f"   Sample party: {entities['parties'][0]}")
        
        return True
    
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False


def test_risk_analysis():
    """Test risk analysis"""
    print("\n" + "="*60)
    print("TEST 4: Risk Analysis")
    print("="*60)
    
    analyzer = ContractAnalyzer()
    test_file = TEMPLATES_DIR / "sample_vendor_contract.txt"
    
    try:
        parse_result = analyzer.parser.parse_document(test_file)
        text = parse_result["text"]
        clauses = analyzer.nlp.extract_clauses(text)
        
        risk_analysis = analyzer.risk_analyzer.analyze_contract_risk(clauses)
        
        print(f"✅ Risk analysis complete")
        print(f"   - Overall risk level: {risk_analysis['overall_risk_level']}")
        print(f"   - Composite score: {risk_analysis['composite_risk_score']}/100")
        print(f"   - High risk clauses: {risk_analysis['risk_distribution']['high']}")
        print(f"   - Medium risk clauses: {risk_analysis['risk_distribution']['medium']}")
        print(f"   - Low risk clauses: {risk_analysis['risk_distribution']['low']}")
        print(f"   - Critical issues: {len(risk_analysis['critical_clauses'])}")
        
        if risk_analysis['composite_risk_score'] > 0:
            return True
        else:
            print("⚠️ Warning: Risk score is 0")
            return False
    
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False


def test_full_analysis_without_llm():
    """Test full analysis pipeline without LLM"""
    print("\n" + "="*60)
    print("TEST 5: Full Analysis (Without LLM)")
    print("="*60)
    
    analyzer = ContractAnalyzer()
    test_file = TEMPLATES_DIR / "sample_vendor_contract.txt"
    
    try:
        print("Running full analysis...")
        result = analyzer.analyze_contract(test_file, use_llm=False)
        
        if result["success"]:
            print(f"✅ Analysis successful!")
            print(f"   - File: {result['file_name']}")
            print(f"   - Clauses: {len(result['clauses'])}")
            print(f"   - Risk score: {result['risk_analysis']['composite_risk_score']}/100")
            print(f"   - Processing time: {result['metadata']['processing_time']:.2f}s")
            return True
        else:
            print(f"❌ Analysis failed: {result.get('error')}")
            return False
    
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_template_generation():
    """Test template generation"""
    print("\n" + "="*60)
    print("TEST 6: Template Generation")
    print("="*60)
    
    from template_generator import TemplateGenerator
    
    try:
        gen = TemplateGenerator()
        templates = gen.list_available_templates()
        
        print(f"✅ Template types available: {len(templates)}")
        for t in templates:
            print(f"   - {t}")
        
        # Test service agreement generation
        parties = {
            "client": "Test Client Ltd",
            "client_address": "Mumbai",
            "provider": "Test Provider",
            "provider_address": "Delhi"
        }
        
        terms = {
            "date": "January 1, 2024",
            "start_date": "January 1, 2024",
            "duration": "12 months",
            "payment": "Rs. 50,000",
            "jurisdiction": "Mumbai"
        }
        
        template = gen.generate_service_agreement(parties, terms)
        
        if len(template) > 100:
            print(f"✅ Service agreement template generated ({len(template)} chars)")
            return True
        else:
            print("❌ Template too short")
            return False
    
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False


def test_knowledge_base():
    """Test knowledge base"""
    print("\n" + "="*60)
    print("TEST 7: Knowledge Base")
    print("="*60)
    
    from knowledge_base import KnowledgeBase
    
    try:
        kb = KnowledgeBase()
        
        # Test statistics
        stats = kb.get_statistics()
        print(f"✅ Knowledge base loaded")
        print(f"   - Total analyses: {stats['total_analyses']}")
        
        # Test common issues
        all_issues = kb.kb["common_issues"]
        total_issues = sum(len(issues) for issues in all_issues.values())
        print(f"   - Common issues documented: {total_issues}")
        
        # Test best practices
        practices = kb.get_best_practices("general")
        print(f"   - Best practices: {len(practices)}")
        
        # Test search
        results = kb.search_knowledge_base("termination")
        print(f"   - Search results for 'termination': {len(results)}")
        
        return True
    
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False


def run_all_tests():
    """Run all tests"""
    print("\n" + "🧪"*30)
    print("CONTRACT ANALYZER - TEST SUITE")
    print("🧪"*30)
    
    tests = [
        ("Document Parsing", test_document_parsing),
        ("Clause Extraction", test_clause_extraction),
        ("Entity Extraction", test_entity_extraction),
        ("Risk Analysis", test_risk_analysis),
        ("Full Analysis (No LLM)", test_full_analysis_without_llm),
        ("Template Generation", test_template_generation),
        ("Knowledge Base", test_knowledge_base),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Test '{test_name}' crashed: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("\n" + "="*60)
    print(f"RESULTS: {passed}/{total} tests passed ({passed*100//total}%)")
    print("="*60)
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! System is ready for demo.")
    elif passed >= total * 0.8:
        print("\n⚠️ Most tests passed. Review failures before demo.")
    else:
        print("\n❌ Multiple failures. System needs fixes.")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
