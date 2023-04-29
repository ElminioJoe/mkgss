def breadcrumb(request):
    breadcrumb = []
    current_path = request.path_info.split('/')[1:]
    for index, path_part in enumerate(current_path):
        # if not path_part:
        #     continue
        url = '/' + '/'.join(current_path[:index + 1]) + '/'
    label = path_part.capitalize().replace('-', ' ')
    breadcrumb.append({'label': label, 'url': url})
    return {'breadcrumb': breadcrumb}