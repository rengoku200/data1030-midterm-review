# Report files

- `Data_Midterm_Report_documented.pdf`: the supplied draft's first four pages followed by the completed data-documentation appendix. Its original empty appendix page was replaced. Main report prose and figures were not edited in this documentation step.
- `appendix_data_documentation.tex`: editable technical reference covering the saved 38 columns, target rules, units, missingness, categorical values, feature roles, and limitations.
- `appendix_standalone.tex`: wrapper for compiling the appendix on its own. Page numbering starts at 5 to match the supplied draft.

## Add the appendix to your LaTeX report

Upload `appendix_data_documentation.tex` to the same Overleaf folder as your main `.tex` file. Make sure the preamble includes these packages (do not load a package twice if it is already present):

```latex
\usepackage{longtable,booktabs,array}
\usepackage[hidelinks]{hyperref}
```

Replace the existing empty appendix section after the references with:

```latex
\clearpage
\onecolumn
\input{appendix_data_documentation.tex}
```

Keep the main report in two columns if desired. The appendix uses one column so the long feature definitions remain readable. Its tables continue across pages. Do not paste the standalone wrapper into the middle of your main document.

To compile the standalone appendix locally from `report/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error appendix_standalone.tex
pdflatex -interaction=nonstopmode -halt-on-error appendix_standalone.tex
```

The documentation was checked against the saved dataset at commit `d4a15bc501564ad6b53e7780ea5cc6976411bb29`. Update the counts and feature-status statements if the data or code changes. The appendix describes historical-count and weekend features as planned because they are not implemented in the committed EDA notebook. It does not repair the collection notebook or validate the original environment.
