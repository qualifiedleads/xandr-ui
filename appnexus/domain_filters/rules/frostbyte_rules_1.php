<?php
if ($cost > 20) {
    if ($conv > 0) { # Conversion is present.
        if ($cpa < 35) {
            $list["whitelist"][] = $domain;
        }
    }
    # Add to blacklist everything that has been processed.
    $list["blacklist"][] = $domain;
}
else {
    if ($conv > 0) {
        # If conversion is present, transfer to whitelist.
        $list["whitelist"][] = $domain;
        $list["blacklist"][] = $domain;
    }
}