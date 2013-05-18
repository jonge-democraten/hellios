from django import template
 
register = template.Library()
 
LEADING_PAGE_RANGE_DISPLAYED = TRAILING_PAGE_RANGE_DISPLAYED = 5
LEADING_PAGE_RANGE = TRAILING_PAGE_RANGE = 3
NUM_PAGES_OUTSIDE_RANGE = 2 
ADJACENT_PAGES = 3
 
def digg_paginator(context, base_url):
    if (context["is_paginated"]):
        in_leading_range = in_trailing_range = False
        pages_outside_leading_range = pages_outside_trailing_range = range(0)

        page_obj = context["page_obj"]
        page = page_obj.number
        num_pages = page_obj.paginator.num_pages
 
        if (num_pages <= LEADING_PAGE_RANGE_DISPLAYED):
            in_leading_range = in_trailing_range = True
            page_numbers = [n for n in range(1, num_pages + 1) if n > 0 and n <= num_pages]           
        elif (page <= LEADING_PAGE_RANGE):
            in_leading_range = True
            page_numbers = [n for n in range(1, LEADING_PAGE_RANGE_DISPLAYED + 1) if n > 0 and n <= num_pages]
            pages_outside_leading_range = [n + num_pages for n in range(0, -NUM_PAGES_OUTSIDE_RANGE, -1)]
        elif (page > num_pages - TRAILING_PAGE_RANGE):
            in_trailing_range = True
            page_numbers = [n for n in range(num_pages - TRAILING_PAGE_RANGE_DISPLAYED + 1, num_pages + 1) if n > 0 and n <= num_pages]
            pages_outside_trailing_range = [n + 1 for n in range(0, NUM_PAGES_OUTSIDE_RANGE)]
        else: 
            page_numbers = [n for n in range(page - ADJACENT_PAGES, page + ADJACENT_PAGES + 1) if n > 0 and n <= num_pages]
            pages_outside_leading_range = [n + num_pages for n in range(0, -NUM_PAGES_OUTSIDE_RANGE, -1)]
            pages_outside_trailing_range = [n + 1 for n in range(0, NUM_PAGES_OUTSIDE_RANGE)]
        return {
            "base_url": base_url,
            "is_paginated": context["is_paginated"],
            "previous": page_obj.previous_page_number,
            "has_previous": page_obj.has_previous,
            "next": page_obj.next_page_number,
            "has_next": page_obj.has_next,
            "page": page_obj.number,
            "pages": page_obj.paginator.num_pages,
            "page_numbers": page_numbers,
            "in_leading_range" : in_leading_range,
            "in_trailing_range" : in_trailing_range,
            "pages_outside_leading_range": pages_outside_leading_range,
            "pages_outside_trailing_range": pages_outside_trailing_range
        }
 
register.inclusion_tag("digg_paginator.html", takes_context=True)(digg_paginator)

