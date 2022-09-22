#!/usr/bin/env python
import click, os, glob
from pikepdf import Pdf

@click.command()
@click.option('--size', default=100, help='Average file size in MB')
@click.option('--file', help='The file to split', required=True)
@click.option('--tmpdir', default="/tmp/moses-tmp", help='Path to tmp directory')
@click.option('--outdir', default="/tmp/moses-out", help='Path to output dir')

def moses(size, file, tmpdir, outdir):
    """Program to split a PDF into chunks by file size."""

    shortname = os.path.basename(file)
    click.echo(f"Splitting {shortname} into chunks by {size}MB.")
    
    outdirexists = os.path.exists(outdir)
    if not outdirexists:
        os.makedirs(outdir)
        click.echo(f"Created output directory at {outdir}.")

    if(outdir[-1:0] != "/"):
        outdir = outdir + "/"

    tmpdirexists = os.path.exists(tmpdir)
    if not tmpdirexists:
        os.makedirs(tmpdir)
        click.echo(f"Created temporary directory at {tmpdir}.")

    if(tmpdir[-1:0] != "/"):
        tmpdir = tmpdir + "/"

    pdf_original = Pdf.open(file)
    for n, page in enumerate(pdf_original.pages):
        dst = Pdf.new()
        dst.pages.append(page)
        dst.save(tmpdir + str(int(f'{n:10}')).zfill(10) + '.pdf')

    filesizes = []
    for chunk in sorted(os.listdir(tmpdir)):
        filesizes.append([chunk, int(os.path.getsize(tmpdir + chunk))])

    totalsize = size * 1000000

    sizeresults = []
    sizes = []
    nameresults = []
    names = []
    for name, value in filesizes:
        if sum(sizes) + value <= totalsize:
            sizes.append(value)
            names.append(name)
        else:
            if sizes:
                sizeresults.append(sizes)
                nameresults.append(names)
            sizes = [value]
            names = [name]
    sizeresults.append(sizes)
    nameresults.append(names)

    counter = 0
    for item in nameresults:
        counter += 1
        pdf = Pdf.new()
        for chunkfile in item:
            src = Pdf.open(tmpdir + chunkfile)
            pdf.pages.extend(src.pages)
        pdf.save(outdir + os.path.basename(file)[:-4] + "-" + str(counter) + ".pdf")

    click.echo(f"Created {counter} chunks in {outdir}.")

    files = glob.glob(tmpdir + '*')
    for f in files:
        os.remove(f)
    
    os.rmdir(tmpdir)

    click.echo(f"Removed temporary directory.")

if __name__ == '__main__':
    moses()
