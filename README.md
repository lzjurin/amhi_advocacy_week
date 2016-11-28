# AMHI Mental Health Advocacy Week
## Overlay Generator

Flask microsite that allows visitors to upload a profile picture and apply filters to it, with a touch of AMHI.

Filters are found in the *filters/* folder, and the filter to be used is specified during startup in *app.py*. Overlays only work if the profile picture is larger in both dimensions than the filter to be applied (no upscaling is done to preserve quality of images). Filters must be of PNG format and transparent on the areas of the profile picture they wish to leave untouched.

######-Larry Zhang
