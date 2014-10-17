<!DOCTYPE HTML>
<%
# 
def hook_def(attribute):
    if hasattr(next, attribute):
        return getattr(next, attribute)
    else:
        return lambda: ""
%>
## <%def name="">
##  Function to check the namespace for `attribute` and renders
## Render attribute.
## ${|n}
## %endif
## </%def>
<html lang="${request.locale_name}">
    <head>
##      Using Bootstrap like a good little automoton.
        <link rel="stylesheet" href="${request.static_url('bicycle_path:static/css/lib/bootstrap.min.css')}">
        <link rel="stylesheet" href="${request.static_url('bicycle_path:static/css/lib/bootstrap-theme.min.css')}">
##      Hook any `style` defs in child template.
        ${hook_def('style')()|n}
    </head>
    <body>
##      Book the child template body.
        ${next.body()|n}
##      Load require.js and our common.js require config.
        <script src="${request.static_url('bicycle_path:static/js/lib/require.min.js')}"></script>
        <script src="${request.static_url('bicycle_path:static/js/common.js')}"></script>
##      Hook any `scripts` defs in child template.
        ${hook_def('scripts')()|n}
    </body>
</html>