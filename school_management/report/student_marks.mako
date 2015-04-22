<html>
    <head>
        <style>
            ${ css }
        </style>
    </head>
    
    <body>
        
        %for obj in objects:
        
        <center> Student Marks </center>
        <br/>
        <br/>
        
        <table width="100%" border="1" class="cell">

             <tr>
                <td class="cell" style="font-size: 12px;font-weight: bold;text-align:left;">
                    Student Name
                </td>
                <td class="cell">
                    ${obj.result_id.name or "" }
                </td>
                <td class="cell" style="font-size: 12px;font-weight: bold;text-align:left;">
                    Subject Name
                </td>
                <td class="cell">
                    ${obj.subject_name or "" }
                </td>
                <td class="cell" style="font-size: 12px;font-weight: bold;text-align:left;">
                    Obtained Marks
                </td>
                <td class="cell">
                    ${obj.obtained_marks or "" }
                </td>
                <td class="cell" style="font-size: 12px;font-weight: bold;text-align:left;">
                    Passing Marks
                </td>
                <td class="cell">
                    ${obj.passing_marks or "" }
                </td>
                <td class="cell" style="font-size: 12px;font-weight: bold;text-align:left;">
                    Maximum Marks
                </td>
                <td class="cell">
                    ${obj.maximum_marks or "" }
                </td>
                <td class="cell" style="font-size: 12px;font-weight: bold;text-align:left;">
                    Final Result
                </td>
                <td class="cell">
                    ${obj.final_result or "" }
                </td>
            </tr>
        </table>
        <br/>
        %endfor
    </body>
</html>