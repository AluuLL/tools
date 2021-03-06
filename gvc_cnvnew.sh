####################################################
#!/usr/bin/bash
#refPath="/disk/Ref/Homo_sapiens/Homo_sapiens_assembly19_fromBroad.fa"
echo "start time:" > map.time
date >> map.time
codePath="/disk/software/GVC-CNV/WES/"
refPath=$1
NBamPath=$2
TBamPath=$3
bedF=$4
bedF1=$5
outID=$6
outpath=$7
if [ $# != 7 ] ; then 
    echo "refPath NBamPath TBamPath bedF bedF1 outID outpath"
    exit 1; 
fi 
####
cd $outpath/
/usr/bin/gvc -n 4  -f $refPath --ghs --cov --snp --in $NBamPath --in $TBamPath --bed $bedF --ccd $bedF1 --out $outID 
echo "/usr/bin/gvc -n 4  -f $refPath --ghs --cov --in $NBamPath --in $TBamPath --bed $bedF --ccd $bedF1 --out $outID"
/disk/software/R-3.3.3/bin/Rscript $codePath/Detect_CNV_CBS.R $outID.cov $outID 0.00001
perl $codePath/join2filesByallMultKeyVOUT.pl $outID.cov $outID.CBS 0,1 1,3 |awk '$6!="-"' -|cut -f 3,6-|awk '{print $2"\t"$3"\t"$4"\t"$1"\t"$6"\t"$7"\t"$8"\t"$9"\t"$10"\t"$11"\t"$12"\t"$13"\t"$14}' > $outID.CBS2
awk '$NF==1' $outID.ghs|cut -f 1-11 > $outID.GHS.gvc2
/disk/software/R-3.3.3/bin/Rscript $codePath/CAScnv_vers6.V2.R $outID.GHS.gvc2 $outID $outID.CBS2 $outID.cov $outID.cov $outpath $codePath
perl -p -e 's/_filtNLOH_1//g' *.filtNegLOH.CN|awk '$NF!=2'|sort -k 1,1 -k 2,2 -k 3,3n|cut -f 1,2,3,4,5,6,11,14-|cat $codePath/header - > $outID.CalledCNV
echo "end time:">> map.time
date>> map.time

