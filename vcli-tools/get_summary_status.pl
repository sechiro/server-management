#!/usr/bin/perl
use strict;
use warnings;
use VMware::VIRuntime;
use JSON;

# usage ./get_summary_status.pl --server 192.168.11.150
my $help_message = "Display type: summary, network, all (default)";
my %opts = (
      display => {
      type => "=s",
      variable => "VI_DISPLAY",
      help => $help_message,
      required => 0,
      },
);

Opts::add_options(%opts);
Opts::parse();
Opts::validate();
my $display_type = defined(Opts::get_option('display')) ? Opts::get_option('display') : 'all';
if ( $display_type !~ /^all$|^summary$|^network$/ ){
    die $help_message;
}
Util::connect();

# Data::Dumper をJSON風に出力
sub json_dumper{
    my $target = shift;
    $Data::Dumper::Indent = 0;  # インデントなし
    $Data::Dumper::Useqq = 1;   # ハッシュのキーはダブルクォートでくくる
    $Data::Dumper::Terse = 1;   # evalするための、最初の「$VAR =」は不要
    $Data::Dumper::Pair = ":";  # ハッシュの区切り文字
    $Data::Dumper::Bless = "";
    my $output = Dumper($target);
    $output =~ s/\(//g;
    $output =~ s/\)//g;
    return $output;
}

# Obtain all inventory objects of the specified type
my $entity_views = Vim::find_entity_views( view_type => 'VirtualMachine' );

# Process the findings and output to the console
foreach my $entity_view (@$entity_views) {
    my $entity_name = $entity_view->name;
    my $vm_summary = $entity_view->summary;
    my $summary_json = json_dumper($vm_summary->guest);
    $summary_json =~ s/, 'VirtualMachineGuestSummary'//;
    $summary_json =~ s/, 'VirtualMachineToolsStatus'//;

    my $net_info_list = $entity_view->guest->net;
    my $net_info_json;
    for my $net_info (@$net_info_list){
        $net_info_json = json_dumper($net_info);
        $net_info_json =~ s/'NetIpConfigInfoIpAddress' ,*//g;
        $net_info_json =~ s/, *'NetIpConfigInfo'//g;
        $net_info_json =~ s/, *]}/ ]}/g;
        $net_info_json =~ s/, *'GuestNicInfo'//g;
        $net_info_json =~ s/, *'NetDnsConfigInfo'//g;
    }

    # Output
    if ( $display_type eq "all" or $display_type eq "summary" ){
        print "{\"$entity_name\":";
        print $summary_json;
        print "}\n";
    }
    if ( $display_type eq "all" or $display_type eq "network" ){
        print "{\"$entity_name\":";
        $net_info_json = defined($net_info_json) ? $net_info_json : '"No guest network information"' ;
        print $net_info_json;
        print "}\n";
    }
}
# Disconnect from the server
Util::disconnect();
