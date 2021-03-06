import os

APPNAME = "plugin.video.blxdtvcatchup"
VERSION = os.environ.get("VERSION") or "0.0.0-SNAPSHOT"
out = "build"


def configure(ctx):
    ctx.check_waf_version(mini='1.9.7')


def build(bld):
    bld(features="subst", source="addon.xml.in", target="addon.xml",
        APPNAME=APPNAME, VERSION=VERSION)
    for f in bld.path.ant_glob('*.txt *.png resources/** lib/*.py addon.py'):
        bld(rule='cp -r ${SRC} ${TGT}',
            source=f,
            target=bld.path.get_bld().make_node(f.relpath()))


def dist(ctx):
    ctx.algo = "zip"
    ctx.base_path = ctx.path.make_node(out)
    ctx.base_name = APPNAME  # set the base directory for the archive
    ctx.arch_name = "{0}-{1}.{2}".format(APPNAME, VERSION, ctx.ext_algo.get(ctx.algo, ctx.algo))
    ctx.files = ctx.path.ant_glob("build/*.xml build/*.txt build/*.py build/*.png build/resources/** build/lib/**")
