pg_dump review_lab > "tvn.dump.out.$(date +%w)"
s3cmd put "tvn.dump.out.$(date +%w)" s3://media.reporterslab.org/beta/tvn/backup/
