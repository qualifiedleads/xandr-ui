<?php
function domain_base($domain)
{
    $pieces = explode('.', $domain);
    $base_name = "";

    if (($size = count($pieces)) > 2)
    {
        if ($size == 3)
        {
            $name = $pieces[0];
            $otld = $pieces[1];
            $ctld = $pieces[2];

            if(strlen($otld) > 3)
            {
                array_shift($pieces);
                $base_name = implode('.', $pieces);
            }
            elseif(strlen($ctld) == 2)
            {
                $base_name = implode('.', $pieces);
            }
            else
            {
                array_shift($pieces);
                $base_name = implode('.', $pieces);
            }
        }
        elseif ($size == 4)
        {
            array_shift($pieces);
            $base_name = implode('.', $pieces);
        }
    }
    else
    {
        $base_name = implode('.', $pieces);
    }

    return $base_name;
}