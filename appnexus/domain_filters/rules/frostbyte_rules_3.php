<?php
if ($conv > 0) { # Conversion is present.
    # Add to whitelist and don't serve in RON campaign.
    $list["whitelist"][] = $domain;
    $list["blacklist"][] = $domain;
}
else {
    # Anything expensive blacklist them.
    $list["blacklist"][] = $domain;
}