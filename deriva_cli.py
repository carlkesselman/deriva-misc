import argparse

from deriva.core import ErmrestCatalog, HatracStore, get_credential
from urllib.parse import urlsplit, urlunsplit


def hatrac_list(args):
    objectstore = args.catalog
    listing = objectstore.retrieve_namespace(args.path)
    for o in listing:
        objectstore.cataget_metadata(o)
        print(o)


def hatrac_copy(args):
    from_path = args.path1
    to_path = args.path2

    if (pa)


def hatrac_namespace(args):
    namespace_path = args.path
    parents = args.parents
    args.catalog.create_namespace(namespace_path, parents)
    print('Created namespace "%s%s".' % (self._server_uri, namespace_path))


def main():
    description = 'DERIVA Command line tool'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--server', help="Hatrac server")

    subparsers = parser.add_subparsers()

    # create the parser for the "list" command
    parser_list = subparsers.add_parser('list', aliases=['ls'])
    parser_list.add_argument('path', nargs='?', default='')
    parser_list.set_defaults(func=hatrac_list)

    # create the parser for the "dir" command
    parser_namespace = subparsers.add_parser('mkdir')
    parser_namespace.add_argument('path')
    parser_namespace.add_argument('-p', default=True)
    parser_namespace.set_defaults(func=hatrac_namespace)

    # copy  file to local directory
    parser_copy = subparsers.add_parser('copy')
    parser_copy.add_argument('path1')
    parser_copy.add_argument('path2')
    parser_copy.set_defaults(func=hatrac_copy)

    # parse the args and call whatever function was selected
    args = parser.parse_args()

    urlparts = urlsplit(args.path, scheme='http')
    host = args.server if args.server else urlparts.netloc
    if host is None:
        print('Hatrac server name required')
        return

    if args.server:
        args.path.replace('/hatrac', '')
        if not args.path.startswith('/'):
            args.path = '/' + args.path
        args.path = '/hatrac' + args.path
    elif args.path == '/hatrac':      # Missing trailing slash
        args.path = '/hatrac/'

    credential = get_credential(host)
    args.catalog = HatracStore(urlparts.scheme, host, credentials=credential)

    args.func(args)


if __name__ == '__main__':
    main()
