#!/usr/bin/env perl

if(scalar(@ARGV)!=2){
	die "args: <sentence> <corpus>\n";
}

#read in a sentence file
open(IN,$ARGV[0]);
while(<IN>){
	chomp;
	push(@sentence,$_);
}
close(IN);

#read in corpus
open(IN,$ARGV[1]);
while(<IN>){
        chomp;
	$line = $_;
	@sentences = split(/\./,$line);
	$numsentences = @sentences;
	if($numsentences == 1)
	{
		push(@corpus,$line);
	}
	else
	{
		for($i = 0; $i<$numsentences;$i++)
		{
			push(@corpus,$sentences[$i]);
		}
	}	
}
close(IN);

#obtain counts
$numsentences = @corpus;
for($j = 0; $j<$numsentences;$j++)
{
	@sentencewords = split(/ /,$corpus[$j]);
	$numsentwords = @sentencewords;
	for($k = 0; $k<$numsentwords; $k++)
	{
		$wordcounts{$sentencewords[$k]}++;
	}
}


#determine probability by number of words that occur in the sentence
$numsentences = @corpus;
@words = split(/ /,$sentence[0]);
$numwords = @words;
for($j = 0; $j<$numsentences;$j++)
{
	@sentencewords = split(/ /,$corpus[$j]);
	$numsentwords = @sentencewords;
	for($i = 0; $i<$numwords; $i++)
	{
		for($k = 0; $k<$numsentwords; $k++)
		{
			if($sentencewords[$k] eq $words[$i])
			{
				$prob_by_count[$j] = $prob_by_count[$j] + (1/$wordcounts{$words[$i]});
			}
		}
	}
}

for($i = 0; $i<10; $i++)
{	
	@top10[$i] = 0;
	@top10sentence[$i] = 0;
}


sub insert
{
	for($i = 0; $i<10; $i++)
	{	
	}
	$x = $_[0];
	$s = $_[1];
	if($x >= $top10[9])
	{
		for($i=9;$i>=0;--$i)
		{
			if($i != 0 && $x >= $top10[$i-1])
			{
				$top10[$i] = $top10[$i-1];
				$top10sentence[$i] = $top10sentence[$i-1];
			}
			else
			{
				$top10[$i] = $x;
				$top10sentence[$i] = $s;
				last;
			}
		}	
	}
}

for($j = 0; $j<$numsentences;$j++)
{
	$totalprob[$j] = $prob_by_count[$j];
}

for($j = 0; $j<$numsentences;$j++)
{
	if($totalprob[$j] eq "")
	{
		insert(0,$corpus[$j]);
	}
	else
	{
		insert($totalprob[$j],$corpus[$j]);
	}
	$numsentences = @corpus;
	for($i = 0; $i<10; $i++)
	{	
		#print($top10sentence[$i]." ".$top10[$i]."\n");
	}
}

$numsentences = @corpus;
for($i = 0; $i<10; $i++)
{
	print($top10sentence[$i]." ".$top10[$i]."\n");
}
