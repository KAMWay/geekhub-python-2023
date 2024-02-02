$(document).ready(function () {
    const $navCarElement = $('#quantityProductCart');
    $(document)
        .on(
            'click', '.addCartButton', (evt) => {
                const target = evt.target;
                const data = {
                    'product_id': target.dataset.product_id,
                    'quantity': 1,
                };
                load(
                    window.cartApiUrl,
                    'POST',
                    data,
                    (result) => {
                        if (target.innerText === 'Remove from cart') {
                            target.classList.remove('btn-warning');
                            target.classList.add('btn-primary');
                            target.innerText = 'Add to cart';
                        } else {
                            target.classList.remove('btn-primary');
                            target.classList.add('btn-warning');
                            target.innerText = 'Remove from cart';
                        }
                        $navCarElement.text(result.items.length);
                    },
                    () => {
                        target.disabled = true;
                    },
                    () => {
                        target.disabled = false;
                    },
                )
            }
        );
    $(document)
        .on(
            'click', '.updateCartButton', (evt) => {
                const target = evt.target;
                const productId = target.dataset.product_id
                const data = productId === null ? {} : getData4Update(productId, parseInt(target.dataset.update_quantity))
                const method = productId === null ? 'DELETE' : 'PUT';
                load(
                    window.cartApiUrl,
                    method,
                    data,
                    (result) => {
                        drawUpdatedCartTable(result)
                        $navCarElement.text(result.items.length);
                    },
                    () => {
                        setTableEventState(target.dataset.product_id, false);
                        // target.attr('disabled', true);
                    },
                    () => {
                        setTableEventState(target.dataset.product_id, true);
                        // target.attr('disabled', false);
                    },
                )
            }
        );

    function getData4Update(productId, updateQuantity) {
        let quantity = 0;
        if (updateQuantity !== 0) {
            quantity = getQuantityFromTable(productId);
            quantity = quantity === null
                ? -1
                : quantity + updateQuantity;
        }

        return {
            'product_id': productId,
            'quantity': quantity,
        }
    }

    function drawUpdatedCartTable(cart) {
        let cartTotal = 0.0;
        $('table tbody tr').each(function () {
            const cellValue = $.trim($(this).find('th').text());
            const itemDict = getCartItemDictByProductId(cart.items, cellValue);
            if (itemDict.length === 0) {
                $(this).remove();
            } else {
                const $priceCell = $(this).find('td:eq(1)');
                const $quantityCell = $(this).find('td:eq(2)');
                const $totalCell = $(this).find('td:eq(3)');

                const total = parseFloat($.trim($priceCell.text())) * itemDict[0].quantity;
                $quantityCell.text(itemDict[0].quantity);
                $totalCell.text(round(total, 2))
                cartTotal += total;
            }
        });

        $('#itemTotalCart').text(round(cartTotal, 2));
    }

    function getQuantityFromTable(searchKey) {
        const quantityArray = $.grep($('table tbody tr'), function (item) {
            return $.trim(item.cells[0].textContent) === searchKey;
        });

        if (quantityArray.length > 0) {
            return parseInt($.trim(quantityArray[0].cells[3].textContent));
        }

        return null;
    }

    function setTableEventState(productId, isEnable) {
        $('table tbody tr').each(function () {
            const itemDict = getCartItemDictByProductId(productId);
            if (itemDict.length > 0) {
                const eventCell = $(this).find('td:eq(4)');
                eventCell.attr('disabled', isEnable);
            }
        });
    }

    function getCartItemDictByProductId(items, searchKey) {
        return $.grep(items, function (item) {
            return item.product_id === searchKey;
        });
    }

    function round(number, count) {
        return parseFloat(number).toFixed(parseInt(count));
    }

    // function drawCartItems(cart) {
    //     let html = '';
    //     $(".detailItemCart").find("button[data-product_id='00932845000P']");
    //
    //     $("tr[data-product_id]")
    //
    //     $.each(cart.items, function (i, item) {
    //
    //         html += '<tr>';
    //         html += '   <th scope="row">';
    //         html += '        <a href="item.product.id"';
    //         html += '           title="Detail info">' + item.product.id + '</a>';
    //         html += '   </th>';
    //         html += '   <td> {0} </td>'.f(item.product.name);
    //         html += '   <td> {0} </td>'.f(item.product.sale_price);
    //         html += '   <td class="text-center fw-bold" id="item_quantity_{{ item.quantity }}">'.f(item.product.sale_price);
    //
    //         html += '   <td class="text-center fw-bold" id="item_quantity_{{ item.quantity }}">';
    //         html += '       {{item.quantity}}';
    //         html += '   </td>';
    //         html += '   <td>{{item.total}}</td>';
    //         html += '   <td>';
    //         html += '       <div className="input-group">';
    //         html += '           <button type="submit" title="plus" className="bi bi-bag-plus nav-link mx-1 updateCartButton"';
    //         html += '                   data-set-product_id="{{ item.product.id }}"';
    //         html += '                   data-set-quantity="{{ item.quantity }}"';
    //         html += '                   data-set-update_quantity="1">';
    //         html += '           </button>';
    //         html += '           <button type="submit" title="dash" className="bi bi bi-bag-dash nav-link updateCartButton"';
    //         html += '                   data-set-product_id="{{ item.product.id }}"';
    //         html += '                   data-set-quantity="{{ item.quantity }}"';
    //         html += '                   data-set-update_quantity="-1">';
    //         html += '           </button>'
    //         html += '           <button type="submit" title="trash" className="nav-link bi bi-trash mx-1 updateCartButton"';
    //         html += '                   data-set-product_id="{{ item.product.id }}"';
    //         html += '                   data-set-quantity="{{ item.quantity }}"';
    //         html += '                   data-set-update_quantity="0">';
    //         html += '           </button>';
    //         html += '       </div>';
    //         html += '   </td>';
    //         html += '</tr>';
    //     });
    // }
});
