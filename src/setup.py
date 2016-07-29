from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup (
	name = 'ParsePcap',
	ext_modules=[
		Extension('parse_pcap', ['parse_pcap.pyx'])
		],
	cmdclass = {'build_ext':build_ext}
)