#!/usr/bin/env perl

#NLP(11-411) 
#Incomplete Script for Assignment on Distributional Similarity
#Author: Michael Heilman (mheilman@cs.cmu.edu)

#This script is meant to calculate semantic similarity values
#among a set of target words.  It first downloads counts for how
#often the feature words occur in the same wikipedia article
#as the target words.  It then creates feature vectors
#using pointwise mutual information.  Finally, it uses a vector
#similarity/distance measure such as Euclidean distance to 
#calculate similarity values between pairs of target words.

if(scalar(@ARGV)!=2){
	die "args: <target word list> <feature word list>\n";
}

#read in list of target words
open(IN,$ARGV[0]);
while(<IN>){
	chomp;
	push(@targetwords,$_);
}
close(IN);

$baseURL="http://www.ark.cs.cmu.edu/NLP/getcount.php";
$totalNumberOfWords = 13000000;
$totalNumberOfPairs = 3000000000;

#read in list of feature words
open(IN,$ARGV[1]);
while(<IN>){
        chomp;
        push(@featurewords,$_);
}
close(IN);

#download total counts for target words
for($i=0;$i<scalar(@targetwords);$i++){
	$tw = $targetwords[$i];
	$url = "$baseURL?w1=$tw&searchtype=opt_doc&mode=quiet";
	$tmpfile = "mytempfile$$";
	$cmd = "wget -q -O '$tmpfile' '$url'";
	#print STDERR "$cmd\n";
	system($cmd);
	open(IN,$tmpfile);
	$output = <IN>;
	close(IN);
	system("rm $tmpfile");
	chomp($output);
	
	#store count in map
	$individualcounts{"$tw"} = $output;
}

#download total counts for feature words
for($j=0;$j<scalar(@featurewords);$j++){
	$fw = $featurewords[$j];
	$url = "$baseURL?w1=$fw&searchtype=opt_doc&mode=quiet";
	$tmpfile = "mytempfile$$";
	$cmd = "wget -q -O '$tmpfile' '$url'";
	#print STDERR "$cmd\n";
	system($cmd);
	open(IN,$tmpfile);
	$output = <IN>;
	close(IN);
	system("rm $tmpfile");
	chomp($output);
	
	#store count in map
	$individualcounts{"$fw"} = $output;
}

#download counts for target, feature words occurring together
for($i=0;$i<scalar(@targetwords);$i++){
	$tw = $targetwords[$i];
	for($j=0;$j<scalar(@featurewords);$j++){
		$fw = $featurewords[$j];
		
		#download count for ith target word and jth feature word
		$url = "$baseURL?w1=$tw&w2=$fw&searchtype=opt_doc&mode=quiet";
		$tmpfile = "mytempfile$$";
		$cmd = "wget -q -O '$tmpfile' '$url'";
		#print STDERR "$cmd\n";
		system($cmd);
		open(IN,$tmpfile);
		$output = <IN>;
		close(IN);
		system("rm $tmpfile");
		chomp($output);
		
		#store count in map
		$paircounts{"$tw\t$fw"} = $output;
	}
}

#print STDERR "COUNTS:\n";
#foreach $key (keys %paircounts){
#	print STDERR "$key\t$paircounts{$key}\n";
#}
#print STDERR "\n";


#calculate PMI, create context feature vectors
for($i=0;$i<scalar(@targetwords);$i++){
        $tw = $targetwords[$i];
	my @curvector = ();
	$contextvectors{%tw} = \@curvector;
        for($j=0;$j<scalar(@featurewords);$j++){
		$fw = $featurewords[$j];
		if($paircounts{"$tw\t$fw"} > 0){		
			$pmi = 999999999;  #<------- WRITE FORMULA HERE
		}else{
			$pmi = 0;
		}
		#print STDERR "$tw\t$fw\t$pmi\n";
		push(@{$contextvectors{$tw}}, $pmi);
	}
}

#calculate similarity based on context feature vectors
for($i=0;$i<scalar(@targetwords);$i++){
	$tw1 = $targetwords[$i];
	@cvec1 = @{$contextvectors{$tw1}};
	for($j=$i+1;$j<scalar(@targetwords);$j++){
		$tw2 = $targetwords[$j];
		@cvec2 = @{$contextvectors{$tw2}};
		
		$distance = 0;
		#
		#		<------- CALCULATE DISTANCE HERE
		#
		#

		#PRINT OUT DISTANCE BETWEEN WORDS (THIS IS NOT A COUNT)
		print "$tw1\t$tw2\t$distance\n";
	}
}

