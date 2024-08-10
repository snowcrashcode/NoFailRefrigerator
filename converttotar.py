import tarfile

# Create a tar.gz archive
with tarfile.open('model.tar.gz', mode='w:gz') as archive:
    archive.add('isolation_forest_model.joblib', arcname='isolation_forest_model.joblib')