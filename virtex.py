#!/usr/bin/env python
import subprocess  
import argparse 

def sh(command):
	print(command)
	subprocess.run(command, shell=True)

parser = argparse.ArgumentParser()
parser.add_argument('ins', help='Input image names', nargs='*')
parser.add_argument('-n', '--number', help='Input column number', type=int, default=2)
parser.add_argument('-o', '--out', help='Input output-filename', type=str)
parser.add_argument('-d', '--dir', help='Input dir-filename', type=str,default=None)
parser.add_argument('--debug', help='debug mode?', action="store_true",default=False)
parser.add_argument('--overpic', help='Input string for overpic', type=str, nargs='*',default=None)
args = parser.parse_args()

N=len(args.ins)
colN=args.number
size=1.0/colN -0.01

if N==0:
	exit()

if (args.overpic==None) or (len(args.overpic)==0):
	overpic=[""]*N
else:
	overpic=args.overpic
	if len(args.overpic)!=N:
		print("Please prepare a list for overpic")
		exit()

temp=r'''
\documentclass[a4paper]{article}
\usepackage[dvipdfmx]{graphicx}
\pagestyle{empty}
\usepackage[percent]{overpic}
\boldmath
\usepackage{txfonts}
\usepackage{geometry}
\geometry{left=10mm,right=10mm,top=30mm,bottom=30mm}
\begin{document}
\begin{figure}
	\centering
'''

for i,im in enumerate(args.ins) :
#	temp+=f"\includegraphics[width={size}\hsize,clip]{{{im}}} "
	print(i,im,overpic[i])
	temp+=fr"\begin{{overpic}}[width={size}\hsize,clip]{{{im}}}"
	temp+=fr"\put(15,52){{\large \bf	{overpic[i]}  }}" 
	temp+=r"\end{overpic}"
	temp+="\\\\" if (i+1)%colN==0 else ""

temp+=r'''
\end{figure}
\end{document}
'''

print(temp)

d     = args.dir if (args.dir != None) else "./"
out   = args.out if (args.out != None) else 'temp'
outtex= out+'.tex'

f=open(d+outtex,'w')
f.write( temp )
f.close()

sh(f"ptex2pdf -l -ot '-synctex=1 -file-line-error' {d}{outtex} -output-directory {d}")
sh(f"pdfcrop {d}{out}.pdf")
if args.debug==False:
	sh(f"rm {d}{out}.aux {d}{out}.log {d}{out}.synctex.gz {d}{out}.pdf")
	sh(f"mv {d}{out}-crop.pdf {d}{out}.pdf")
