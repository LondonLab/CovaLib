#!/bin/csh

foreach i (`cat dirlist`)
cd $i
    qsub /home/dinad/CovaLib/Code/single_job_submission.sh
cd ..
end


