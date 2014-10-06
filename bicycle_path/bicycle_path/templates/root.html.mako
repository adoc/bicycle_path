<!DOCTYPE HTML>
<html lang="${request.locale_name}">
    <head>
        <link rel="stylesheet" href="${request.static_url('bicycle_path:static/css/bootstrap.min.css')}">
        <link rel="stylesheet" href="${request.static_url('bicycle_path:static/css/bootstrap-theme.min.css')}">
    </head>
    <body>
        ${next.body()}
        <script src="${request.static_url('bicycle_path:static/js/lib/jquery.min.js')}"></script>
        <script src="${request.static_url('bicycle_path:static/js/lib/bootstrap.min.js')}"></script>
        <script src="${request.static_url('bicycle_path:static/js/site.js')}"></script>
        %if hasattr(next, 'scripts'):
        ${next.scripts()|n}
        %endif
    </body>
</html>