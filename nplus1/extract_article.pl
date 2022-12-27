my $path = $ARGV[0];
my $input = `cat $path`;

while ($input =~ /<div class="n1_material text-18"><p class="mb-6">(.*?)<\/p><\/div>/gs) {
    $v = $1;
    $v =~ s/<a.*?>//g;
    $v =~ s/<\/a>//g;
    $v =~ s/<iframe.*?>//g;
    $v =~ s/<\/iframe>//g;
    print $v;
}
