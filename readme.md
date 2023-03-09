Vector Search for finding Similar Documents.
============================================

This is a sample application made to test out vector search in a  real life application. It makes use of
dual databases consisting of MySQL and Pinecone for storing data and for storing corresponding vectors 
respectively. This application is serced using a Django application with a few sections to test, view and
add documents or reports. To run the application, make a ``.env`` file in the same format as 
``.env.sample`` provided alongside the project (or just rename the sample file), and fill it with 
appropriate keys. Then, use start.bat (or run the Django app provided in ``api``). Scripts to load the data
in same format as provided [here][dataset], use ``data_loader.py`` and to make sample documents to test the 
app, use ``make_sample.py`` in the root directory.


[dataset]: https://www.kaggle.com/datasets/alizahidraja/covid19-allresearchpapers-lemmatizedinformation
