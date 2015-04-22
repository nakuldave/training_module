<html>
    <head>
        <style>
            ${ css }
        </style>
    </head>
    
    <body>
        
        %for obj in objects:
        
        <center> Sale Information </center>
        <br/>
        <br/>
        
        <table width="100%" border="1" class="cell">

             <tr>
                <td class="cell" style="font-size: 12px;font-weight: bold;text-align:left;">
                    Sale Order No
                </td>
                <td class="cell">
                    ${obj.name or "" }
                </td>
                <td class="cell" style="font-size: 12px;font-weight: bold;text-align:left;">
                    Customer
                </td>
                <td class="cell">
                    ${obj.customer_id.name or "" }
                </td>
                <td class="cell" style="font-size: 12px;font-weight: bold;text-align:left;">
                    Date
                </td>
                <td class="cell">
                    ${obj.date or "" }
                </td>
                <td class="cell" style="font-size: 12px;font-weight: bold;text-align:left;">
                    Customer Reference
                </td>
                <td class="cell">
                    ${obj.customer_ref or "" }
                </td>
            </tr>
        </table>
        <br/>
        
        <table width="100%" border="1" class="cell">
            <tr>
            <td class="cell" style="font-size: 12px;font-weight: bold;text-align:center;">
                  Product
            </td>
                <td class="cell" style="font-size: 12px;font-weight: bold;text-align:center;">
                  Description
                </td>
                <td class="cell" style="font-size: 12px;font-weight: bold;text-align:center;">
                  Price 
                </td>
                <td class="cell" style="font-size: 12px;font-weight: bold;text-align:center;">
                  Quantity 
                </td>
                <td class="cell" style="font-size: 12px;font-weight: bold;text-align:center;">
                  Sub Total 
                </td>
            </tr>
            %for line in obj.order_line_ids:
                 <tr>
                   <td class="cell" >
                       ${line.product_id.name} 
                    </td>
                    <td class="cell" >
                      ${line.name or ""} 
                    </td>
                    <td class="cell">
                      ${line.unit_price or 0.0} 
                    </td>
                    <td class="cell">
                       ${line.qty or 0.0} 
                    </td>
                    <td class="cell">
                      ${line.sub_total or 0.0}
                    </td>
                </tr>
            %endfor
            
        %endfor
        </table>
    </body>
</html>