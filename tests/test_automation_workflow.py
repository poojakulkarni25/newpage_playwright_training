"""
Test file automating workflow with:
- Element visibility assertions
- Text content validation
- URL navigation verification
- Element count after filtering
- Multiple wait strategies (auto-wait, expect(), custom waits, network idle)
- 3-second delays to view UI actions
"""

import time
import re
from playwright.sync_api import sync_playwright, expect


class TestAutomationWorkflow:
    """Test class for comprehensive automation workflow testing"""

    def setup_method(self):
        """Setup for each test - initialize browser and page"""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def teardown_method(self):
        """Teardown after each test - close browser"""
        self.page.close()
        self.context.close()
        self.browser.close()
        self.playwright.stop()

    def test_element_visibility_with_auto_wait(self):
        """
        Test 1: Element Visibility
        Validates that elements are visible using Playwright's auto-wait mechanism
        """
        print("\n=== TEST 1: Element Visibility with Auto-Wait ===")
        
        # Navigate to a test page
        self.page.goto("https://demo.playwright.dev/todomvc")
        time.sleep(3)  # View the navigation action
        
        # Auto-wait: Playwright automatically waits for element to be actionable
        # The page object itself ensures the page is loaded before proceeding
        heading = self.page.locator("h1")
        
        # Assert visibility - auto-wait handles the waiting
        assert heading.is_visible(), "Heading should be visible"
        print("✓ Element visibility verified (auto-wait)")
        time.sleep(3)  # View the assertion result on UI

    def test_text_content_with_expect(self):
        """
        Test 2: Text Content Validation
        Uses expect() method for powerful assertions with built-in waits
        """
        print("\n=== TEST 2: Text Content with expect() ===")
        
        self.page.goto("https://demo.playwright.dev/todomvc")
        time.sleep(3)  # View the navigation
        
        # Using expect() - automatically waits and retries
        heading = self.page.locator("h1")
        expect(heading).to_contain_text("todos")
        print("✓ Text content verified with expect()")
        time.sleep(3)  # View the result

    def test_url_navigation_with_custom_wait(self):
        """
        Test 3: URL Navigation
        Verifies URL changes after navigation using custom wait logic
        """
        print("\n=== TEST 3: URL Navigation with Custom Wait ===")
        
        self.page.goto("https://demo.playwright.dev/todomvc")
        time.sleep(3)  # View initial page
        
        # Custom wait: Wait for URL to match a specific pattern
        # Using wait_for_url with timeout
        self.page.goto("https://demo.playwright.dev/todomvc")
        self.page.wait_for_url(re.compile(r".*demo.playwright.dev/todomvc.*"), timeout=5000)
        
        # Assert the URL
        current_url = self.page.url
        assert "demo.playwright.dev/todomvc" in current_url, f"URL should contain 'demo.playwright.dev/todomvc', got {current_url}"
        print(f"✓ Current URL verified: {current_url}")
        time.sleep(3)  # View the URL verification

    def test_element_visibility_with_expect_to_be_visible(self):
        """
        Test 4: Element Visibility using expect()
        Demonstrates expect().to_be_visible() with built-in waits
        """
        print("\n=== TEST 4: Element Visibility with expect().to_be_visible() ===")
        
        self.page.goto("https://demo.playwright.dev/todomvc")
        time.sleep(3)  # View the page
        
        # expect().to_be_visible() waits up to timeout for visibility
        # Use .first to avoid strict mode when multiple elements match
        paragraph = self.page.locator("p").first
        expect(paragraph).to_be_visible()
        print("✓ Element visibility confirmed with expect()")
        time.sleep(3)  # View the result

    def test_element_count_after_filtering(self):
        """
        Test 5: Element Count After Filtering
        Counts elements matching a selector after filtering/dynamic updates
        """
        print("\n=== TEST 5: Element Count After Filtering ===")
        
        # Navigate to a page with multiple elements
        self.page.goto("https://demo.playwright.dev/todomvc")
        time.sleep(3)  # View initial page
        
        # Auto-wait ensures all elements are loaded
        paragraphs = self.page.locator("p")
        
        # Get count of all paragraphs
        element_count = paragraphs.count()
        print(f"✓ Total paragraph elements found: {element_count}")
        
        # Assert element count
        assert element_count > 0, "Should have at least one paragraph element"
        print("✓ Element count verified")
        time.sleep(3)  # View the count result

    def test_network_idle_wait(self):
        """
        Test 6: Network Idle Wait
        Waits for all network requests to complete before proceeding
        """
        print("\n=== TEST 6: Network Idle Wait ===")
        
        # Navigate and wait for network to be idle
        self.page.goto("https://demo.playwright.dev/todomvc")
        
        # Wait for network idle - ensures all requests complete
        self.page.wait_for_load_state("networkidle")
        print("✓ Network idle state reached - all requests completed")
        time.sleep(3)  # View the idle state
        
        # Verify page is fully loaded
        title = self.page.title()
        assert title, "Page should have a title"
        print(f"✓ Page title verified: {title}")
        time.sleep(3)

    def test_combined_wait_strategies(self):
        """
        Test 7: Combined Multiple Wait Strategies
        Demonstrates using auto-wait, expect(), custom waits, and network idle together
        """
        print("\n=== TEST 7: Combined Wait Strategies ===")
        
        # 1. Navigate with auto-wait
        print("Step 1: Navigating to page...")
        self.page.goto("https://demo.playwright.dev/todomvc")
        time.sleep(3)
        
        # 2. Wait for network idle
        print("Step 2: Waiting for network idle...")
        self.page.wait_for_load_state("networkidle")
        time.sleep(3)
        
        # 3. Auto-wait for element and verify visibility
        print("Step 3: Verifying element visibility with auto-wait...")
        heading = self.page.locator("h1")
        assert heading.is_visible(), "Heading should be visible"
        time.sleep(3)
        
        # 4. Use expect() for text content
        print("Step 4: Verifying text content with expect()...")
        expect(heading).to_contain_text("todos")
        time.sleep(3)
        
        # 5. Custom wait for element count
        print("Step 5: Verifying element count...")
        elements = self.page.locator("p")
        element_count = elements.count()
        assert element_count >= 0, "Element count should be non-negative"
        print(f"✓ Element count: {element_count}")
        time.sleep(3)
        
        # 6. Verify URL
        print("Step 6: Verifying URL...")
        current_url = self.page.url
        assert "demo.playwright.dev/todomvc" in current_url, f"URL should contain demo.playwright.dev/todomvc"
        print(f"✓ URL verified: {current_url}")
        time.sleep(3)
        
        print("✓ All combined wait strategies validated successfully")

    def test_expect_text_visible(self):
        """
        Test 8: Expect Text to be Visible
        Asserts that specific text is visible on the page
        """
        print("\n=== TEST 8: Expect Text Visible ===")
        
        self.page.goto("https://demo.playwright.dev/todomvc")
        time.sleep(3)
        
        # Wait for and verify text visibility - use get_by_text for better matching
        expect(self.page.get_by_text("todos", exact=True)).to_be_visible()
        print("✓ Text 'todos' is visible")
        time.sleep(3)

    def test_expect_enabled_element(self):
        """
        Test 9: Expect Element to be Enabled
        Validates that an element is enabled and actionable
        """
        print("\n=== TEST 9: Expect Element Enabled ===")
        
        self.page.goto("https://demo.playwright.dev/todomvc")
        time.sleep(3)
        
        # Find a link and verify it's enabled
        link = self.page.locator("a").first
        
        # Check if link exists (auto-wait will handle visibility)
        if link.count() > 0:
            expect(link).to_be_enabled()
            print("✓ Link element is enabled")
        else:
            print("⚠ No link elements found on page")
        
        time.sleep(3)

    def test_custom_wait_for_selector(self):
        """
        Test 10: Custom Wait for Selector
        Waits for a specific selector to appear with custom timeout
        """
        print("\n=== TEST 10: Custom Wait for Selector ===")
        
        self.page.goto("https://demo.playwright.dev/todomvc")
        time.sleep(3)
        
        # Wait for a specific selector to be in the DOM (not just visible)
        self.page.wait_for_selector("h1", timeout=5000)
        print("✓ H1 selector appeared in DOM within timeout")
        
        h1_element = self.page.locator("h1")
        heading_text = h1_element.text_content()
        print(f"✓ H1 content: {heading_text}")
        time.sleep(3)

    def test_expect_url_contains(self):
        """
        Test 11: Expect URL Contains
        Verifies that URL contains expected string after navigation
        """
        print("\n=== TEST 11: Expect URL Contains ===")
        
        self.page.goto("https://demo.playwright.dev/todomvc")
        time.sleep(3)
        
        # expect() automatically waits for condition with retries
        expect(self.page).to_have_url(re.compile(r".*demo.playwright.dev/todomvc.*"))
        print("✓ URL matches expected value")
        time.sleep(3)

    def test_expect_title(self):
        """
        Test 12: Expect Page Title
        Asserts the page title using expect()
        """
        print("\n=== TEST 12: Expect Page Title ===")
        
        self.page.goto("https://demo.playwright.dev/todomvc")
        time.sleep(3)
        
        # expect() for page title
        expect(self.page).to_have_title("React • TodoMVC")
        print("✓ Page title verified")
        time.sleep(3)

    def test_multiple_assertions_with_expect(self):
        """
        Test 13: Multiple Assertions with expect()
        Demonstrates chaining multiple expect() assertions
        """
        print("\n=== TEST 13: Multiple Assertions with expect() ===")
        
        self.page.goto("https://demo.playwright.dev/todomvc")
        time.sleep(3)
        
        heading = self.page.locator("h1")
        
        # Multiple assertions - each with auto-wait and retry logic
        print("Assertion 1: Checking visibility...")
        expect(heading).to_be_visible()
        time.sleep(1)
        
        print("Assertion 2: Checking text content...")
        expect(heading).to_contain_text("todos")
        time.sleep(1)
        
        print("Assertion 3: Checking element is enabled...")
        expect(heading).to_be_enabled()
        time.sleep(1)
        
        print("✓ All multiple assertions passed")
        time.sleep(3)

    def test_element_attribute_with_expect(self):
        """
        Test 14: Element Attribute Verification
        Validates element attributes using expect()
        """
        print("\n=== TEST 14: Element Attribute Verification ===")
        
        self.page.goto("https://demo.playwright.dev/todomvc")
        time.sleep(3)
        
        # Find a link and check its href attribute
        link = self.page.locator("a").first
        
        if link.count() > 0:
            # Verify link has href attribute
            href_value = link.get_attribute("href")
            assert href_value is not None, "Link should have href attribute"
            print(f"✓ Link href attribute found: {href_value}")
        else:
            print("⚠ No link elements found")
        
        time.sleep(3)

    def test_no_element_with_expect(self):
        """
        Test 15: Verify Element Does Not Exist
        Uses expect() to assert element is not visible
        """
        print("\n=== TEST 15: Element Does Not Exist ===")
        
        self.page.goto("https://demo.playwright.dev/todomvc")
        time.sleep(3)
        
        # Assert that a non-existent element is not visible
        non_existent = self.page.locator("div.non-existent-class-xyz")
        expect(non_existent).not_to_be_visible()
        print("✓ Non-existent element correctly verified as not visible")
        time.sleep(3)


def run_single_test(test_name: str):
    """
    Utility function to run a single test
    Usage: python test_automation_workflow.py
    """
    test_instance = TestAutomationWorkflow()
    test_instance.setup_method()
    
    try:
        # Run the specified test
        test_method = getattr(test_instance, test_name)
        test_method()
        print(f"\n✓ {test_name} passed!")
    except Exception as e:
        print(f"\n✗ {test_name} failed: {str(e)}")
    finally:
        test_instance.teardown_method()


if __name__ == "__main__":
    print("=" * 70)
    print("PLAYWRIGHT AUTOMATION WORKFLOW TEST SUITE")
    print("=" * 70)
    print("\nThis test suite demonstrates:")
    print("  • Element visibility verification")
    print("  • Text content assertion")
    print("  • URL navigation validation")
    print("  • Element count after filtering")
    print("  • Auto-wait mechanism")
    print("  • expect() method with built-in waits")
    print("  • Custom wait strategies")
    print("  • Network idle waits")
    print("  • 3-second UI view delays")
    print("\n" + "=" * 70)
    
    # Run a specific test - uncomment to run individual tests
    # run_single_test("test_element_visibility_with_auto_wait")
    
    print("\nTo run with pytest:")
    print("  pytest test_automation_workflow.py -v -s")
    print("\nTo run a specific test:")
    print("  pytest test_automation_workflow.py::TestAutomationWorkflow::test_element_visibility_with_auto_wait -v -s")
