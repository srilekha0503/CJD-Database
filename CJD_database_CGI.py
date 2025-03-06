#!/usr/bin/env python3

import cgi
import cgitb
import pymysql
from string import Template

#Enable CGI traceback
cgitb.enable()
print("Content-type: text/html\n")

#Create html home page
#leave space for the style, title, intro, form, summary, table, error message
html_home_page = Template(
"""
<html>    
    <head>
        <title>CJD Database</title>
        <link rel="icon" href="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/Boston_University_seal.svg/280px-Boston_University_seal.svg.png" type="image/x-icon">

        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/chosen/1.8.7/chosen.min.css">
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/chosen/1.8.7/chosen.jquery.min.js"></script>
        <link rel="stylesheet" href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.min.css">
        <script src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>

        ${style}
    </head>

    <body>
        <!--Create header for all pages in the website-->
        <div class="page-header">
            <div class="page-header-logo">
                <img src="https://www.bu.edu/brand/files/2019/06/master_logo.gif">
            </div>
            <div class="page-header-text">
                <h1>CJD Database</h1>
            </div>
            <!-- The following drop down menu uses AJAX to display -->
            <div class="menu-dropdown">
                <a style="text-decoration: none; margin-right: 25px; color: gray;" href="#" onclick="display_home()">HOME</a>
                <a style="text-decoration: none; margin-right: 25px; color: gray;" href="#" onclick="load_content('https://bioed.bu.edu/students_24/Team_12/about.html')">ABOUT</a>
                <a style="text-decoration: none; margin-right: 25px; color: gray;" href="#" onclick="load_content('https://bioed.bu.edu/students_24/Team_12/upload.html')">UPLOAD</a>
                <a style="text-decoration: none; color: gray;" href="#" onclick="load_content('https://bioed.bu.edu/students_24/Team_12/help.html')">HELP</a>
            </div>
        </div>
        
        <!--Display AJAXed page content-->
        <div id="page-content"></div>

        <!--Home page body content-->
        <div class="search" id="home-content">
            <div class="search-form">
		        <h2>Fill out search parameters</h2>
		        ${html_form}
	        </div>
	        <div id='table_output'>
		        ${table_output}
	        </div>
            <div style="display:flex; flex-direction:column;"> 
                <div id="pie_chart_div" style="width: 800px; height: 400px;"></div>
                <div id="bar_chart_div" style="width: 800px; height: 400px;"></div>
            </div>
            <script>

            window.onload = ()=>{
            
                //Google Charts library
                google.charts.load('current', {'packages':['corechart']}); 
                google.charts.setOnLoadCallback(drawChart);
                google.charts.setOnLoadCallback(drawBar);
                
                //Function to draw the pie chart
                function drawChart() {
                    var pie_data = (${pie_data_str});
                    var data = google.visualization.arrayToDataTable(pie_data);
                    var options = {
                    title: 'Distribution of Annotations for the given Impact and Biotype',
                    width: 800,
                    height: 400,
                    is3D: true};
                    var chart = new google.visualization.PieChart(document.getElementById('pie_chart_div'));
                    chart.draw(data, options);

                }

                function drawBar() {
                    var bar_data = (${bar_data_str});
                    var data = google.visualization.arrayToDataTable(bar_data);
                    var options = {
                    title: 'Distribution of Biotype for the given Annotations and Impact',
                    width: 800,
                    height: 400};
                    var chart = new google.visualization.BarChart(document.getElementById('bar_chart_div'));
                    chart.draw(data, options);
                }

            }
            </script>
        </div>


        <script>
            //Function to display home page when the home tab is clicked
            function display_home() {
		        document.getElementById('home-content').classList.remove('hidden');
                document.getElementById('page-content').classList.add('hidden');
            }

            // AJAX function to dynamically load the home, about, upload, and help pages
            function load_content(page) {
                var xhttp = new XMLHttpRequest();
                xhttp.onreadystatechange = function() {
                    if (this.readyState == 4 && this.status == 200) {
                        document.getElementById('page-content').classList.remove('hidden');
                        document.getElementById('page-content').innerHTML = this.responseText;

                        // Hide undesired page content when other pages are loaded
                        if (page == 'https://bioed.bu.edu/students_24/Team_12/about.html') {
                            document.getElementById('home-content').classList.add('hidden');
                            document.getElementById('about-content').classList.remove('hidden');
                            document.getElementById('upload-content').classList.add('hidden');
                            document.getElementById('help-content').classList.add('hidden');
                        }
                        if (page == 'https://bioed.bu.edu/students_24/Team_12/upload.html') {
                            document.getElementById('home-content').classList.add('hidden');
                            document.getElementById('about-content').classList.add('hidden');
                            document.getElementById('upload-content').classList.remove('hidden');
                            document.getElementById('help-content').classList.add('hidden');
                        
                        }
                        if (page == 'https://bioed.bu.edu/students_24/Team_12/help.html') {
                            document.getElementById('home-content').classList.add('hidden');
                            document.getElementById('about-content').classList.add('hidden');
                            document.getElementById('upload-content').classList.add('hidden');
                            document.getElementById('help-content').classList.remove('hidden');
                        }
                    }
                };
                xhttp.open('GET', page, true);
                xhttp.send();
            }

            $(document).ready(function() {
                $('#columns-returned').chosen({
                    width:"300px"
                })
            })

	        $(document).ready(function() {
                $('#annotation-selector').chosen({
                    width:"300px"
                })
            })
	        $(document).ready(function() {
                $('#impact').chosen({
                    width:"300px"
                })
            })
            $(document).ready(function() {
                $('#biotype').chosen({
                    width:"300px"
            })
        })
          	    
	    //Function to send input file to be parsed
	    function postData() {
		const file_input = document.getElementById('file-input');
                const file = file_input.files[0];

                if (!file) {
                    alert('Please select a file to upload.');
                    return;
                }
	    }

        //Datatable
        $(document).ready(function() {
            // Create and display data table
            $('#data_table').DataTable({
                "paging": true // Enable pagination
            });

            //Download datatable on button click
            $('#download-btn').on('click', function() {
                //Get data from datatable
                var data = $('#data_table').data().toArray();

                //Convert data to CSV format
                var csv_content = 'data:text/csv;charset=utf-8,';
                data.forEach(function(row) {
                    csv_content += row.join(',') + '&#10;';
                });

                //Create download link
                var encodedURI = encodeURI(csv_content);
                var link = document.createElement('a');
                link.setAttribute('href', encodedURI);
                link.setAttribute('download', 'CJD_query.csv');
                document.body.appendChild(link);

                //Trigger download
                link.click();

                //Clean up
                document.body.removeChild(link);
            });
        });
	</script>
    </body>
</html>
"""
)

style = """
        <style>
            .hidden {
                display: none;
            }
            .page-header {
                display: flex;
                align-items: center;
                background-color: white;
                padding: 10px 20px;
                box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
                font-family: Arial, Helvetica, sans-serif;
            }
            .page-header-logo {
                margin: 5px;
            }
            .page-header-text {
                margin: 0;
                color: gray;
                font-size: 20px;
                margin-left: 10px;
            }
            .menu-dropdown {
                margin-left: auto;
                margin-right: 30px;
                color: gray;
                font-size: 20px;
            }
            .search {
                font-family: Arial, Helvetica, sans-serif;
                font-size: 20px;
		    text-align: center;
                padding: 10px;
                margin: 10px;
            }
	        .search-form {
		        background-color: lightgray;
	        }
            table {
                width: 90%;
                border: 1px solid;
                border-collapse: collapse;
            }
            th, td {
                padding: 5px;
                text-align: center;
                border: 1px solid;
            }
            tr:hover {background-color: lightblue;}
            .column-selector {
                display: flexbox;
		        margin: 30px;
		        text-align: center;
            }
            th {
                background-color: lightblue;
                color: white;
            }
	        h3 {
		        font-size: 25px;
		        text-align: center;
		        margin-top: 50px;
	        }
            .chosen-container-multi .chosen-choices{
                min-height: 30px;
            }
            .about-content {
                font-family: Arial, Helvetica, sans-serif;
                font-size: 20px;
            }
            .about-header {
                margin: 20px;
                text-align: center;
                color: gray;
            }
            .about-body {
                text-align: center;
                color: black;
		    margin: 60px;
            }
            .upload-content {
                font-family: Arial, Helvetica, sans-serif;
                font-size: 20px;
            }
            .upload-header {
                margin: 20px;
                text-align: center;
                color: gray;
            }
            .upload-body {
                text-align: center;
                color: gray;
            }
            .help-content {
                font-family: Arial, Helvetica, sans-serif;
            }
            .help-header {
                text-align: center;
                font-size: 20px;
                color: gray;
            }
        </style>
"""

html_form = """
<form>
    <div class="filter-selector">
	<label for="annotation-selector">Annotation:</label>
	<select id="annotation-selector" name="annotation-selector" multiple>
            <option value="intron_variant">intron_variant</option>
            <option value="upstream_gene_variant">upstream_gene_variant</option>
            <option value="downstream_gene_variant">downstream_gene_variant</option>
            <option value="3_prime_UTR_variant">3_prime_UTR_variant</option>
            <option value="5_prime_UTR_variant">5_prime_UTR_variant</option>
            <option value="non_coding_transcript_exon_variant">non_coding_transcript_exon_variant</option>
            <option value="disruptive_inframe_deletion">disruptive_inframe_deletion</option>
            <option value="conservative_inframe_insertion">conservative_inframe_insertion</option>
            <option value="missense_variant">missense_variant</option>
            <option value="synonymous_variant">synonymous_variant</option>
            <option value="intergenic_region">intergenic_region</option>
            <option value="conservative_inframe_deletion">conservative_inframe_deletion</option>
            <option value="frameshift_variant">frameshift_variant</option>
            <option value="splice_region_variant">splice_region_variant</option>
            <option value="disruptive_inframe_insertion">disruptive_inframe_insertion</option>
            <option value="start_retained_variant">start_retained_variant</option>
            <option value="5_prime_UTR_premature_start_codon_gain_variant">5_prime_UTR_premature_start_codon_gain_variant</option>
            <option value="stop_gained">stop_gained</option>
            <option value="non_coding_transcript_variant">non_coding_transcript_variant</option>
            <option value="intragenic_variant">intragenic_variant</option>
            <option value="start_lost">start_lost</option>
            <option value="stop_retained_variant">stop_retained_variant</option>
            <option value="bidirectional_gene_fusion">bidirectional_gene_fusion</option>
            <option value="stop_lost">stop_lost</option>
        </select>

        <label for="patient">Patient:</label>
	    <input type="text" id="patient" name="patient">


	<br><br>

	<label for="impact">Impact:</label>
	<select id="impact" name="impact" multiple>
	    <option value="modifier">MODIFIER</option>
	    <option value="low">LOW</option>
	    <option value="moderate">MODERATE</option>
	    <option value="high">HIGH</option>
	</select>

	<br><br>

	<label for="gene_name">Gene name:</label>
	<input type="text" id="gene_name" name="gene_name">

	<label for="biotype">Biotype:</label>
	<select id="biotype" name="biotype" multiple>
	    <option value="protein_coding">protein_coding</option>
	    <option value="retained_intron">retained_intron</option>
            <option value="nonsense_mediated_decay">nonsense_mediated_decay</option>
            <option value="pseudogene">pseudogene</option>
            <option value="processed_transcript">processed_transcript</option>
            <option value="miRNA">miRNA</option>
            <option value="transcribed_processed_pseudogene">transcribed_processed_pseudogene</option>
            <option value="transcribed_unprocessed_pseudogene">transcribed_unprocessed_pseudogene</option>
            <option value="non_stop_decay">non_stop_decay</option>
            <option value="misc_RNA">misc_RNA</option>
            <option value=""></option>
            <option value="processed_pseudogene">processed_pseudogene</option>
            <option value="TEC">TEC</option>
            <option value="transcribed_unitary_pseudogene">transcribed_unitary_pseudogene</option>
            <option value="snRNA">snRNA</option>
            <option value="snoRNA">snoRNA</option>
            <option value="rRNA">rRNA</option>
            <option value="unprocessed_pseudogene">unprocessed_pseudogene</option>
            <option value="ribozyme">ribozyme</option>
            <option value="polymorphic_pseudogene">polymorphic_pseudogene</option>
            <option value="unitary_pseudogene">unitary_pseudogene</option>
            <option value="scaRNA">scaRNA</option>
	</select>

	<br><br>
	
	<label for="chromosome">Chromosome:</label>
	<input type="text" id="chromosome" name="chromosome">

	<label for="position">Position:</label>
	<input type="text" id="position" name="position">

	<label for="quality">Quality:</label>
	<input type="text" id="quality" name="quality">

	<br><br>
    </div>

    <div>
    <input type="submit" value="Submit">
    <button id="download-btn">Download</button>
    </div>	
</form>
"""

table_output = ""
pie_data_str=""
bar_data_str=""

#Retrieve data
form = cgi.FieldStorage(keep_blank_values=False)


#Check form submission
if (form):
    #Get submitted values
    annotation = form.getvalue("annotation-selector")
    patient = form.getvalue("patient")
    impact = form.getvalue("impact")
    gene_name = form.getvalue("gene_name")
    biotype = form.getvalue("biotype")
    chromosome = form.getvalue("chromosome")
    position = form.getvalue("position")
    quality = form.getvalue("quality")

    query = """
    select variant_name, gene_name, feature_type, a.alternate_allele
    from Annotations a join Variant using (vid)
    where a.annotation = %s and a.impact = %s and a.biotype = %s  
    """

    pie_chart_query = """
    SELECT annotation 
    FROM Annotations
    WHERE impact = %s AND biotype = %s;
    """

    bar_chart_query = """
    SELECT biotype
    FROM Annotations a
    WHERE annotation = %s and impact = %s
    """

    #Establish database connection
    try:
        connection = pymysql.connect(
            host='bioed.bu.edu',
            user='dbreton',
            password='Branquinho',
            db='Team_12',
            port=4253
        )
    except pymysql.Error as e:
        print(e)

    #Create cursor object
    cursor = connection.cursor()
    
    #execute query
    try:
        cursor.execute(query,[annotation,impact,biotype])
    except pymysql.Error as e:
        print(e)
  
    #fetch results
    results = cursor.fetchall()
  
    try:
        cursor.execute(pie_chart_query,[impact, biotype])
    except pymysql.Error as e:
        print(e)

    #fetch results of pie chart
    pie_chart_results = cursor.fetchall()
    

    #execute bar chart query
    try:
        cursor.execute(bar_chart_query, [annotation, impact])
    except pymysql.Error as e:
        print(e)

    #fetch results of bar chart
    bar_chart_results = cursor.fetchall()
    #don't forget to close cursor and mysql connection
    cursor.close()
    connection.close()
  
    table_output = ""
  
    if (results):
        table_output = Template(
        """
        <table id="data_table">
            <thead> 
                <th>Variant Name</th>
                <th>Gene Name</th>
                <th>Feature Type</th>
                <th>Alternate Allele</th>
            </thead>
            <tbody>
                ${table_rows}
            </tbody>
        </table>
        """
        )
    
        #now create the rows
        table_rows = ""
        for row in results:
            table_rows += """ 
                    <tr>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                    </tr>
            """ % (row[0],row[1],row[2], row[3])

        #add rows to table_output
        table_output = table_output.safe_substitute(table_rows=table_rows)

        

    else:
      table_output = "No results to display."

    if pie_chart_results:
        pie_data = [['Category', 'Count']]
        value_counts = {}  #Dictionary to store counts of each value

        #Count occurrences of each value
        for row in pie_chart_results:
            value = row[0]
            if value in value_counts:
                value_counts[value] += 1
            else:
                value_counts[value] = 1

        # Add data rows for each value and its count
        for value, count in value_counts.items():
            pie_data.append([value, count])

        pie_data_str = json.dumps(pie_data)

    else:
        pie_data_str = "No results to display"


    if bar_chart_results:
        bar_data = [['Category', 'Count']]
        bar_value_counts = {}

        for row in bar_chart_results:
            value = row[0]
            if value in bar_value_counts:
                bar_value_counts[value] += 1
            else:
                bar_value_counts[value] = 1

        # Add data rows for each value and its count
        for value, count in bar_value_counts.items():
            bar_data.append([value, count])

        bar_data_str = json.dumps(bar_data)

    else:
        bar_data_str = "No results to display"


#Substitute values
html_output = html_home_page.safe_substitute(style=style, html_form=html_form, table_output=table_output, pie_data_str=pie_data_str, bar_data_str=bar_data_str)

print(html_output)
