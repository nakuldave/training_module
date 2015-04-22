<html>
    <head>
        <style>
            ${ css }
        </style>
    </head>
    
    <body>
        
        %for obj in objects:
        
        <center> ${company.name or ""} </center>
        <center> Sale Order </center>
        <br/>
        <br/>
        <table width="100%" border="1" class="cell">
            <tr>
                <td class="cell" style="font-size: 12px;font-weight: bold;text-align:left;">
                 Order Reference
                </td>
                <td class="cell">
                ${ obj.name or ""}
                </td>
                <td class="cell" style="font-size: 12px;font-weight: bold;text-align:left;">
                Date
                </td>
                <td class="cell">
                ${ obj.date_order}
                </td>
            </tr>
             <tr>
                <td class="cell" style="font-size: 12px;font-weight: bold;text-align:left;">
                Shop
                </td>
                <td class="cell">
                ${obj.shop_id and obj.shop_id.name or "" }
                </td>
                <td class="cell" style="font-size: 12px;font-weight: bold;text-align:left;">
                Customer Reference
                </td>
                <td class="cell">
                ${ obj.client_order_ref or ""}
                </td>
            </tr>
             <tr>
                <td class="cell" style="font-size: 12px;font-weight: bold;text-align:left;">
                    Email                
                </td>
                <td class="cell">
                    ${obj.email or "" }
                </td>
                <td class="cell" style="font-size: 12px;font-weight: bold;text-align:left;">
                    Contact
                </td>
                <td class="cell">
                    ${obj.contact or "" }
                </td>
            </tr>
        </table>
        <br/>
        <table width="100%" border="1" class="cell">
            <tr>
            <td class="cell" style="font-size: 12px;font-weight: bold;text-align:center;">
                Sr.No.
            </td>
                <td class="cell" style="font-size: 12px;font-weight: bold;text-align:center;">
                   Description          
                </td>
                <td class="cell" style="font-size: 12px;font-weight: bold;text-align:center;">
                    Quantity
                </td>
                <td class="cell" style="font-size: 12px;font-weight: bold;text-align:center;">
                    Discount
                </td>
                <td class="cell" style="font-size: 12px;font-weight: bold;text-align:center;">
                    Unit Price
                </td>
                <td class="cell" style="font-size: 12px;font-weight: bold;text-align:center;">
                    Sub Total
                </td>
            </tr>
            %for line,no in zip(obj.order_line, serial(obj.order_line)):
                 <tr>
                   <td class="cell" >
                       ${no}          
                    </td>
                    <td class="cell" >
                       ${ line.name or ""}          
                    </td>
                    <td class="cell">
                        ${line.product_uom_qty or 0.0}
                    </td>
                    <td class="cell">
                        ${line.discount or 0.0}
                    </td>
                    <td class="cell">
                        ${line.price_unit or 0.0 }
                    </td>
                    <td class="cell">
                        ${line.price_subtotal or 0.0}
                    </td>
                </tr>
            %endfor
        
        </table>
        %endfor
        
    </body>
</html>