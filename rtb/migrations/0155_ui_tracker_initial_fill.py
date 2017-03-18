from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rtb', '0154_ui_report_initial_fill'),
    ]

    operations = [

        #
        # impression tracker
        #

        migrations.RunSQL("""
                DROP INDEX  IF EXISTS rtb_impression_tracker_cpid;
                CREATE INDEX rtb_impression_tracker_cpid ON rtb_impression_tracker USING btree ("CpId");
                """),

        migrations.RunSQL("""
                    DROP INDEX  IF EXISTS rtb_impression_tracker_date;
                    CREATE INDEX rtb_impression_tracker_date ON rtb_impression_tracker USING btree ("Date");
                    """),

        migrations.RunSQL("""
                            DROP INDEX  IF EXISTS rtb_impression_tracker_cpid_date;
                            CREATE INDEX rtb_impression_tracker_cpid_date ON rtb_impression_tracker USING btree ("CpId", "Date");
                            """),

        migrations.RunSQL("""
                        DROP INDEX  IF EXISTS rtb_impression_tracker_aucid;
                        CREATE INDEX rtb_impression_tracker_aucid ON rtb_impression_tracker USING btree ("AuctionId");
                        """),

        migrations.RunSQL("""
                            DROP INDEX  IF EXISTS rtb_impression_tracker_advid;
                            CREATE INDEX rtb_impression_tracker_advid ON rtb_impression_tracker USING btree ("AdvId");
                            """),

        #
        # click tracker
        #

        migrations.RunSQL("""
                    DROP INDEX  IF EXISTS rtb_click_tracker_cpid;
                    CREATE INDEX rtb_click_tracker_cpid ON rtb_click_tracker USING btree ("CpId");
                    """),

        migrations.RunSQL("""
                        DROP INDEX  IF EXISTS rtb_click_tracker_date;
                        CREATE INDEX rtb_click_tracker_date ON rtb_click_tracker USING btree ("Date");
                        """),

        migrations.RunSQL("""
                            DROP INDEX  IF EXISTS rtb_click_tracker_cpid_date;
                            CREATE INDEX rtb_click_tracker_cpid_date ON rtb_click_tracker USING btree ("CpId", "Date");
                            """),

        migrations.RunSQL("""
                            DROP INDEX  IF EXISTS rtb_click_tracker_aucid;
                            CREATE INDEX rtb_click_tracker_aucid ON rtb_click_tracker USING btree ("AuctionId");
                            """),

        migrations.RunSQL("""
                                DROP INDEX  IF EXISTS rtb_click_tracker_advid;
                                CREATE INDEX rtb_click_tracker_advid ON rtb_click_tracker USING btree ("AdvId");
                                """),

        #
        # conversion tracker
        #

        migrations.RunSQL("""
                    DROP INDEX  IF EXISTS rtb_conversion_tracker_cpid;
                    CREATE INDEX rtb_conversion_tracker_cpid ON rtb_conversion_tracker USING btree ("CpId");
                    """),

        migrations.RunSQL("""
                        DROP INDEX  IF EXISTS rtb_conversion_tracker_date;
                        CREATE INDEX rtb_conversion_tracker_date ON rtb_conversion_tracker USING btree ("Date");
                        """),

        migrations.RunSQL("""
                        DROP INDEX  IF EXISTS rtb_conversion_tracker_cpid_date;
                        CREATE INDEX rtb_conversion_tracker_cpid_date ON rtb_conversion_tracker USING btree ("CpId", "Date");
                        """),

        migrations.RunSQL("""
                            DROP INDEX  IF EXISTS rtb_conversion_tracker_aucid;
                            CREATE INDEX rtb_conversion_tracker_aucid ON rtb_conversion_tracker USING btree ("AuctionId");
                            """),

        migrations.RunSQL("""
                                DROP INDEX  IF EXISTS rtb_conversion_tracker_advid;
                                CREATE INDEX rtb_conversion_tracker_advid ON rtb_conversion_tracker USING btree ("AdvId");
                                """),

    ]