#!/usr/bin/perl -w
#从file2文件中删除第key2列中带file1中第keys1-cols内容的行。join2filesByallMultKeyVOUT.pl Genelist ANKL.ampliseq.CASpoint.GVC.final.xls 0 0|awk '$1!="-" && $2!="-"'|cut -f 2-|less -S
use strict;
#.pl file1 file2 keys1-cols(,) keys2 out-file
#pick file1 file2 all
if (@ARGV!=4) {
	die ".pl file1 file2 keys1-cols(,) keys2\n";
}
my @arrayKey1=split(/,/,$ARGV[2]);
my @arrayKey2=split(/,/,$ARGV[3]);
my @array;
my $key;
my %hash;
my %hash2;
my $flag=0;
my $num;
my $num2;

open (IN,$ARGV[0])||die ("Could not open file $ARGV[0]\n");
while (<IN>) {
	chomp $_;
	@array=split(/\s+/,$_);
	if ($flag==0) {
		$num=scalar @array;
		$flag=1;
	}

	
	for (my $i=0;$i<@arrayKey1 ;$i++) {
		$key.=$array[$arrayKey1[$i]]."-";
	}
	$hash{$key}=$_;
	$key="";
}
if ($flag==0) {
die ("$ARGV[0] is null\n");
}
close IN;
open IN,$ARGV[1];
#open (OUT,">$ARGV[4]")||die ("Could not open file $ARGV[4]\n");
$flag=0;
while (<IN>) {
	@array=split(/\s+/,$_);
	if ($flag==0) {
		$num2=scalar @array;
		$flag=1;
	}
	for (my $i=0;$i<@arrayKey2 ;$i++) {
		$key.=$array[$arrayKey2[$i]]."-";
	}
	if ($hash{$key}) {
		print "$hash{$key}\t$_";
		$hash2{$key}=1;
	}
	else {
		for (my $i=0;$i<$num ;$i++) {
			print "-\t";
		}
		print "$_";
	}
	$key="";
}
foreach my $aa (keys %hash) {
		if ($hash2{$aa}) {
			next;
		}
	print $hash{$aa},"\t";
	for (my $i=0;$i<$num2-1 ;$i++) {
			print "-\t";
	}
		print "-\n";
}
close IN;
