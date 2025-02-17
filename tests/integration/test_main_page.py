from time import sleep
import logging

from dash_docs.chapter_index import URL_TO_CONTENT_MAP

logger = logging.getLogger(__name__)


def test_snap001_index_page_links(dash_doc, index_pages):
    dash_doc.wait_for_element(".toc .toc--chapter-content")
    dash_doc.percy_snapshot("index - 1")
    bad_links = []

    good_links = ['/', '/search']

    for resource in index_pages:
        if resource.startswith('/'):
            hook_id = "wait-for-page-{}".format(resource)
            res = resource.lstrip("/")
            if res in ['getting-started-part-2', 'datatable/callbacks']:
                # these two pages have an intermittent problem with their
                # resource queues not clearing properly. While we sort this out,
                # just wait a reasonably long time on these pages.
                # code copied out of dash.testing.browser & modified
                # if we end up wanting to keep this we can add a sleep time to
                # the visit_and_snapshot signature.
                dash_doc.driver.get(
                    "{}/{}".format(dash_doc.server_url.rstrip("/"), res)
                )
                dash_doc.wait_for_element_by_id(hook_id)
                sleep(3)
                dash_doc.percy_snapshot(res, wait_for_callbacks=False)
                assert not dash_doc.driver.find_elements_by_css_selector(
                    "div.dash-debug-alert"
                ), "devtools should not raise an error alert"
            else:
                dash_doc.visit_and_snapshot(res, hook_id=hook_id, stay_on_page=True)

            linked_paths = dash_doc.driver.execute_script(
                'return Array.from(document.querySelectorAll(\'a[href^="/"]\'))'
                '.map(a=>a.attributes.href.value)'
            )
            for link in linked_paths:
                if link not in URL_TO_CONTENT_MAP and link not in good_links:
                    msg = '{} --- on page {}'.format(link, resource)
                    logger.info(msg)
                    bad_links.append(msg)

            dash_doc.driver.back()

    assert bad_links == []


def test_snap002_external_resources(dash_doc):
    driver = dash_doc.driver
    resource = "/external-resources"
    driver.get(dash_doc.server_url + resource)
    dash_doc.wait_for_element_by_id("wait-for-page-{}".format(resource))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    dash_doc.percy_snapshot(resource)


def test_snap003_search(dash_doc):
    dash_doc.driver.get(dash_doc.server_url + "/search")
    dash_doc.wait_for_element_by_id("search-input")
    dash_doc.percy_snapshot("search-blank")
    search = dash_doc.find_element("#search-input")
    dash_doc.clear_input(search)
    search.send_keys("dropdown")
    dash_doc.wait_for_element("#hits .ais-hits--item")
    dash_doc.percy_snapshot("search-dropdown")
