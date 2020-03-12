def reg(cn, equiv):
    copies = int(cn)
    eq = equiv.lower() == 'true'
    if eq:
        if copies == 0:
            # Equivocal Loss
            return -1
        else:
            # Equivocal Amplification
            return 1
    else:
        if copies == 0:
            # Not Equivocal Loss
            return -2
        else:
            # Not Equivocal Loss
            return 2


# Here we're keeping a dictionary of
# gene : {sample : copy-number}
def generate_cnv(paths, iID, p_ident, s_ident, cnvs, keys):
    sample = "GENIE-{}-{}-{}".format(iID, p_ident, s_ident)
    keys.append(sample)

    for path in paths:
        values = {sample: str(reg(path.attr("copy-number"), path.attr("equivocal")))}

        try:
            cnvs[path.attr("gene")].update(values)
        except KeyError:
            cnvs[path.attr("gene")] = values


def output_cnvs(iID, cnvs, keys):
    outfile = "data_CNA_{}.txt".format(iID)

    with open(outfile, 'w') as out:
        print("Hugo_Symbol", *keys, file=out, sep="\t")

        for gene, values in cnvs.items():
            print(gene,
                  "\t".join(values[key] if key in values
                            else "0" for key in keys),
                  file=out, sep="\t")
