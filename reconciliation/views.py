import pandas as pd
from django.shortcuts import render
from process.reconcile import pre_process, reconcile

from reconciliation.forms import CSVUploadForm


def process_file(source, target):
    """
    This is the main function used to reconcile data

    Parameters
    ----------
    source : File
        Source file .
    target : File
        Target file.

    Returns
    -------
    Dict
        The difference between source and target files

    """
    source_df = pd.read_csv(source, index_col=0, skipinitialspace=True)
    target_df = pd.read_csv(target, index_col=0, skipinitialspace=True)

    cleaned_source_df, cleaned_target_df = pre_process(source_df, target_df)
    difference = reconcile(cleaned_source_df, cleaned_target_df)

    return difference


def reconciliation_view(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            source_file, target_file = request.FILES.values()
            difference = process_file(source_file, target_file)
            return render(request, "report.html", {"difference": difference})
    else:
        form = CSVUploadForm()

    return render(
        request,
        "reconciliation_page.html",
        {"form": form, "errors": form.errors},
    )
