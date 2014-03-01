.. _api:

================================================================================
Developer Interface
================================================================================

This part of the documentation covers all the interfaces of PennCourseReview.

``apps``
================================================================================

PennCourseReview consists of three packages:

1. ``pcr_detail``
   
2. ``searchbar``
   
3. ``static``

``apps/pcr_detail``
--------------------------------------------------------------------------------

``apps/pcr_detail`` is responsible for serving model detail pages (ie, the
instructor page, the coursehistory page, and the department page). Each page
consists of three widgets:

* An "infobox" (Top-left). The infobox is responsible for showing information
  about the model itself. Since infoboxes change dramatically based on the
  model, there are different templates for each model.

* A scorecard (Top-right). The scorecard is responsible for showing the average
  and recent values of the reviews.

* A "scoretable" (Bottom). The scoretable is responsible for displaying the raw
  reviews in an accessible manner. The scoretable is composed by grouping on a
  key object (either a course or an instructor) and then displaying a relevant
  "sectiontable" which displays the raw data and possibly has a comment.

* A "choose_cols_box" (Visible when you click "Choose Columns"). The
  choose_cols_box is responsible for formatting the attributes into two columns.

This app also contains models.py which contains wrappers for each of the API
objects.

``apps/searchbar``
--------------------------------------------------------------------------------

``apps/searchbar`` is responsible for the backend code that powers the searchbar.

``apps/static``
--------------------------------------------------------------------------------

``apps/static`` is responsible for serving the FAQ and About page. Both of these
pages actually have their content stored in the API (so that admins only have to
manage one site).

``lib/api``
================================================================================

Each of these apps make use of the api function found in lib/api/api.py. The api
function pulls domain and token data from sandbox_config to make requests to the
PCR API.
